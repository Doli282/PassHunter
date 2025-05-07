"""Uploader - uploading files to OpenSearch """
import base64
import datetime
import logging
import os

from celery import Celery
from opensearchpy import helpers

from celeryconfig import ConfigUploader

# Import OpenSearch
from opensearch.opensearch import Client

# Set up logging
LOGGING_FORMAT = '%(asctime)s Monitor: %(levelname)s: %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)

# Celery - Uploader
uploader = Celery('uploader')
uploader.config_from_object(ConfigUploader)

# OpenSearch client
opensearch = Client()

@uploader.task(name='uploader.upload_batch')
def upload_batch(folder_path: str):
    # Get the timestamp of the upload.
    upload_time = datetime.datetime.now().isoformat()
    upload_bulk(folder_path, upload_time)
    # Upload the files with individual API calls.
    #for file in os.listdir(folder_path):
    #    upload_file(os.path.join(folder_path, file), upload_time)

    # TODO perform search
    # TODO alerting
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


def search_batch(uploaded_at: str = None) -> Any:

    logging.debug("searching")
    # TODO add access to the database
    TERM = 'bautista4455'
    response = opensearch.search_term(TERM, uploaded_at)
    return response

# TODO remove
print("-"*20 + "UPLOADING" + "-"*20)
upload_t = upload_batch("/home/doli/bp/BP-application/monitor/test_data")
print("-"*20 + "SEARCHING" + "-"*20)
print(search_batch(upload_t))
print("-"*20 + "DELETING" + "-"*20)
opensearch.indices.delete(index=opensearch.index_id)
