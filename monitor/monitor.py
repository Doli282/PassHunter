"""Uploader - uploading files to OpenSearch """
import base64
import datetime
import logging
import os

from celery import Celery
from opensearchpy import helpers
from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from config import ConfigUploader, Config
from opensearch.opensearch import Client

from models import Alert, Domain, Watchlist

# Set up logging
LOGGING_FORMAT = '%(asctime)s Monitor: %(levelname)s: %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)

# Celery - Uploader
uploader = Celery('uploader')
uploader.config_from_object(ConfigUploader)

# OpenSearch client
opensearch = Client()

# Engine for connecting to the database.
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)

@uploader.task(name='monitor.process_batch')
def process_batch(folder_path: str):
    # Get the timestamp of the upload.
    upload_time = datetime.datetime.now()
    logging.info(f"Processing a new batch from '{folder_path}' at {upload_time.isoformat()}")
    # Upload all files in the folder to OpenSearch.
    upload_bulk(folder_path, upload_time.isoformat())
    # Search for the domains in the uploaded batch.
    search_batch(upload_time)
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

def upload_bulk(folder_path: str, upload_time: str) -> None:
    """
    Upload all files in a folder to OpenSearch in one API call.

    Args:
        folder_path (str): The path to the folder.
        upload_time (str): The upload time.

    Returns:
        None
    """
    # List of actions to be taken care of during the API call to OpenSearch.
    actions = []
    # Iterate over all files in the folder.
    for file in os.listdir(folder_path):
        # Encode the data for upload.
        encoded_data = None
        with open(os.path.join(folder_path, file), "rb") as f:
            encoded_data = base64.b64encode(f.read()).decode('utf-8')

        # If the data could not be read, return False.
        if not encoded_data:
            logging.error("Could not read data from file")
            continue

        # Add the document upload to actions.
        actions.append(opensearch.prepare_bulk_upload(encoded_data, file, upload_time))

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
            hit_count = search_for_domain(domain, uploaded_at)
            logging.debug(f"Domain found {hit_count} times.")
            # When the domain is found, create alerts for each watchlist associated with the domain.
            if hit_count > 0:
                make_alerts(domain, uploaded_at, session)

def search_for_domain(domain: 'Domain', uploaded_at: datetime.datetime) -> int:
    """
    Search for a domain in OpenSearch.
    Searches for the domain name only in the uploaded batch.

    Args:
        domain (Domain): The domain to search for.
        uploaded_at (datetime): The timestamp of the upload.

    Returns:
        Hit count.
    """
    logging.debug(f"Searching for domain: '{domain.name}'")
    # Search for the domain with OpenSearch.
    response = opensearch.search_term(domain.name, uploaded_at.isoformat())
    # Check if the domain was found.
    return response.get("hits", {}).get("total", {}).get("value", 0)

def make_alerts(domain: 'Domain', created_at: datetime.datetime, session: Session) -> None:
    """
    Make alerts for the domain.
    Iterate over watchlists and raise alerts.

    Args:
        domain (Domain): The domain for which alerts should be created.
        created_at (datetime): The creation time of the alert.
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
        alert = Alert(is_new=True, created_at=created_at, domain=domain, watchlist=watchlist)
        session.add(alert)
        session.commit()
        logging.info(f"Alert created for domain '{domain.name}' and watchlist '{watchlist.name}'")
        # Send an email alert if configured.
        if watchlist.send_alerts and watchlist.email:
            logging.debug(f"Sending alert for domain '{domain.name}' and watchlist '{watchlist.name}' to '{watchlist.email}'")
            # TODO send email alert
            # TODO send alert into Slack (or something like that)


# TODO remove
print("-"*20 + "UPLOADING" + "-"*20)
upload_t = process_batch("./test_data")
print("-"*20 + "DELETING" + "-"*20)
opensearch.indices.delete(index=opensearch.index_id)
