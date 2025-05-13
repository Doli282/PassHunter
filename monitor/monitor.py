"""Uploader - uploading files to OpenSearch """
import base64
import datetime
import hashlib
import logging
import os
import shutil
import smtplib
from email.message import EmailMessage
from http.client import responses

from celery import Celery
from opensearchpy import helpers
from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from config import ConfigUploader, Config
from opensearch.opensearch import Client

from models import Alert, Domain, File, Watchlist

# Set up logging
LOGGING_FORMAT = '%(asctime)s Monitor: %(levelname)s: %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, level=os.getenv("LOGGING_LEVEL", "INFO"))

# Celery - Uploader
uploader = Celery('uploader')
uploader.config_from_object(ConfigUploader)

# OpenSearch client
opensearch = Client()

# Engine for connecting to the database.
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

@uploader.task(name='monitor.process_batch')
def process_batch(directory_name: str):
    directory_path = os.path.join(Config.DATA_PATH, directory_name)
    # Get the timestamp of the upload.
    upload_time = datetime.datetime.now(datetime.timezone.utc)
    logging.info(f"Processing a new batch from '{directory_name}' at {upload_time.isoformat()}")
    # Upload all files in the folder to OpenSearch.
    upload_bulk(directory_path, upload_time.isoformat())
    # Search for the domains in the uploaded batch.
    try:
        search_batch(upload_time)
    except Exception as e:
        logging.error(f"Error searching for domains in the uploaded batch: {e}")
    # Clean uploaded data
    try:
        shutil.rmtree(directory_path)
    except Exception as e:
        logging.error(f"Error cleaning uploaded data: {e}")
    return upload_time

def upload_file(file_path: str, upload_time: str) -> bool:
    """
    Upload a file to OpenSearch.

    Args:
        file_path (str): The path to the file.
        upload_time (str): The upload time.

    Returns:
        bool: True if the file was uploaded successfully, False otherwise.
    """
    logging.debug(f"Uploading file '{file_path}'")
    # Read data from the file and encode it to base64
    encoded_data = None
    with open(file_path, "rb") as file:
        encoded_data = base64.b64encode(file.read()).decode('utf-8')

    # If the data could not be read, return False
    if not encoded_data:
        logging.error("Could not read data from file")
        return False

    # Index the document using the pipeline
    try:
        filename = os.path.basename(file_path)
        opensearch.upload_file(encoded_data, filename, upload_time)
        logging.debug(f"File '{filename}' uploaded successfully")
        return True
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        return False

def upload_bulk(directory_path: str, upload_time: str) -> None:
    """
    Upload all files in a folder to OpenSearch in one API call.

    Args:
        directory_path (str): The path to the folder.
        upload_time (str): The upload time.

    Returns:
        None
    """
    # List of actions to be taken care of during the API call to OpenSearch.
    actions = []
    # Iterate over all files in the folder.
    for file in os.listdir(directory_path):
        try:
            file_path = os.path.join(directory_path, file)

            # Check if the file already exists in the database.
            exists, digest = check_hash_in_db(file_path)
            if exists:
                logging.debug(f"File '{file}' already exists in the database (hash={digest.hex()}). Skipping.")
                continue
            # Encode the data for upload.
            encoded_data = None
            with open(file_path, "rb") as f:
                encoded_data = base64.b64encode(f.read()).decode('utf-8')

            # If the data could not be read, return False.
            if not encoded_data:
                logging.error("Could not read data from file")
                continue

            # Save the file to the database
            create_file(file, digest)
            # Add the document upload to actions.
            actions.append(opensearch.prepare_bulk_upload(encoded_data, file, upload_time))
        except Exception as e:
            logging.error(f"Error uploading file '{file}': {e}")
            continue
    # Perform the bulk upload.
    success = 0
    try:
        success, _ = helpers.bulk(opensearch, actions, raise_on_error=True, request_timeout=60)
    except helpers.BulkIndexError:
        logging.error(f"Error during bulk indexing")
    if success != len(actions):
        logging.error(f"Not all documents were indexed. Success rate: ({success}/{len(actions)})")
    else:
        logging.info(f"Successfully uploaded {success} documents.")

def search_batch(uploaded_at: datetime.datetime) -> None:
    """
    Search for domains in the uploaded batch.

    Args:
        uploaded_at (datetime): The timestamp of the upload.

    Returns:
        None
    """
    logging.debug(f"Searching through the batch uploaded at {uploaded_at.isoformat()}")
    # Get the list of monitored domains.
    statement = select(Domain).filter(Domain.watchlists.any(Watchlist.is_active==True))
    with Session(engine) as session:
        # Search for each domain in the batch.
        for domain in session.scalars(statement).all():
            try:
                hit_count, highlights = search_for_domain(domain, uploaded_at)
                logging.debug(f"Domain found {hit_count} times.")
                # When the domain is found, create alerts for each watchlist associated with the domain.
                if hit_count > 0:
                    make_alerts(domain, uploaded_at, highlights, session)
            except Exception as e:
                logging.error(f"Error searching for domain '{domain.name}': {e}")
                continue

def search_for_domain(domain: 'Domain', uploaded_at: datetime.datetime = None) -> tuple[int, dict[list[str]]]:
    """
    Search for a domain in OpenSearch.
    Searches for the domain name only in the uploaded batch.

    Args:
        domain (Domain): The domain to search for.
        uploaded_at (datetime): The timestamp of the upload.

    Returns:
        Tuple of hit count and list of lists for highlighted matches.
    """
    logging.debug(f"Searching for domain: '{domain.name}'")
    # Search for the domain with OpenSearch.
    response = opensearch.search_term(domain.name, uploaded_at.isoformat() if isinstance(uploaded_at, datetime.datetime) else uploaded_at)
    logging.debug(f"Search response: {response}")
    # Check if the domain was found.
    # Save all matches
    hits = response.get("hits", {}).get("hits", [])
    matches = {}
    for hit in hits:
        matches[hit.get("_source", {}).get("filename", "unknown")] = hit.get("highlight", {}).get("attachment_parts", [])
    return response.get("hits", {}).get("total", {}).get("value", 0), matches

def make_alerts(domain: 'Domain', created_at: datetime.datetime, content: dict[list[str]], session: Session) -> None:
    """
    Make alerts for the domain.
    Iterate over watchlists and raise alerts.

    Args:
        domain (Domain): The domain for which alerts should be created.
        created_at (datetime): The creation time of the alert.
        content (dict[list[str]]): The dict of highlighted matches.
        session (Session): The database session.

    Returns:
        None
    """
    logging.debug(f"Creating alerts for domain: '{domain.name}'")
    # When the domain is found, create alerts for each watchlist associated with the domain.
    for watchlist in domain.watchlists:
        if not watchlist.is_active:
            # If the watchlist is not active, skip it.
            logging.debug(f"Watchlist [{watchlist.id}] '{watchlist.name}' is not active. Skipping.")
            continue
        # Create an alert for the watchlist.
        try:
            alert = Alert(is_new=True, created_at=created_at, content=content, domain=domain, watchlist=watchlist)
            session.add(alert)
            session.commit()
            logging.info(f"Alert created for domain '{domain.name}' and watchlist '{watchlist.name}'")
        except Exception as e:
            logging.error(f"Error creating alert for domain '{domain.name}' and watchlist '{watchlist.name}': {e}")
        # Send an email alert if configured.
        if watchlist.send_alerts and watchlist.email:
            try:
                send_email(watchlist.email, domain.name, watchlist.name, created_at.strftime("%Y-%m-%d %H:%M UTC"))
            except Exception as e:
                logging.error(f"Error sending email alert to {watchlist.email}: {e}")

def check_hash_in_db(file: str) -> tuple[bool, bytes | None]:
    """
    Check if the file already exists in the database.
    Checks the files' hashes.

    Args:
        file (str): The file to check.

    Returns:
        tuple[bool, bytes | None]: A tuple containing a boolean indicating whether the file exists in the database, and the file's hash if it does.
    """
    digest = None
    # Calculate the hash of the file.
    with open(file, "rb") as f:
        digest = hashlib.file_digest(f, 'sha512').digest()

    # If the hash could not be calculated, return True.
    if not digest:
        logging.error("Could not calculate hash of file")
        return True, None

    # Check if the hash already exists in the database.
    with Session(engine) as session:
        file = session.scalar(select(File).where(File.hash == digest))
        # If the file already exists, return True.
        if file:
            logging.debug(f"File '{file.name}' already exists in the database.")
            return True, digest
    return False, digest

def create_file(filename: str, digest: bytes) -> File:
    """
    Create a new file in the database.

    Args:
        filename (str): The name of the file.
        digest (bytes): The hash of the file.

    Returns:
        File: The created file.
    """
    file = File(name=filename, hash=digest)
    with Session(engine) as session:
        session.add(file)
        session.commit()
    return file

def send_email(receiver_address: str, domain_name: str, watchlist_name: str, detected_at: str) -> None:
    """
    Send an alert via email using SMTP_SSL

    Args:
        receiver_address (str): The email address of the receiver.
        domain_name (str): The name of the domain for which the alert was raised.
        watchlist_name (str): The name of the watchlist which generated the alert.
        detected_at (str): The timestamp of the alert.

    Returns:
        None
    """
    subject = "[PassHunter] Alert - domain found!"
    body = f"""\
    Hello,

    A domain from your watchlist has just been detected in newly discovered leaked data.

    • Domain: {domain_name}  
    • Watchlist: {watchlist_name}
    • Detected: {detected_at}

    This may indicate that credentials or sensitive information related to this domain have been exposed.

    Recommend reaction:
    - Reset passwords or access credentials if applicable
    - Monitor suspicious activity
    - Investigate the possible source of the leak

    Stay safe,  
    — PassHunter
    """

    # Prepare the email message
    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = os.getenv("EMAIL_SENDER")
    message['To'] = receiver_address
    message.set_content(body)

    logging.info(f"Sending alert for domain '{domain_name}' and watchlist '{watchlist_name}' to '{receiver_address}'")
    # Send the email using SMTP_SSL
    with smtplib.SMTP_SSL(host=Config.SMTP_SERVER, port=Config.SMTP_PORT) as smtp:
        smtp.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
        smtp.send_message(message)
        return
