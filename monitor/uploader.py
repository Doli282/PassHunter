"""Uploader - uploading files to OpenSearch """
import base64
import datetime
import logging
import os

from celery import Celery
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
pipeline = 'txt_pipeline'
opensearch = Client(init_pipeline=pipeline)

@uploader.task(name='uploader.upload_batch')
def upload_batch(folder_path: str):
    for file in os.listdir(folder_path):
        upload_file(os.path.join(folder_path, file))

def upload_file(file_path: str):

    logging.debug(f"Uploading file '{file_path}'")
    # TODO maybe divide the file manually with python (split by lines)
    # Read data from the file and encode it to base64
    encoded_data = None
    with open(file_path, "rb") as file:
        encoded_data = base64.b64encode(file.read()).decode('utf-8')

    # If the data could not be read, return False
    if not encoded_data:
        logging.error("Could not read data from file")
        return False

    # Prepare the document to be uploaded
    document = {
        "data": encoded_data,
        "filename": os.path.basename(file_path),
        "uploaded_at": datetime.datetime.now(datetime.UTC).isoformat()
    }

    # Index the document using the pipeline
    # TODO maybe use bulk indexing
    response = opensearch.index(index="documents", pipeline=pipeline, body=document)
    print(response)
    return True

def search_batch():
    logging.debug("searching")
    # TODO add access to the database
    TERM = 'pass'
    response = opensearch.search_term(TERM)
    print(response)

# TODO remove
print("-"*20 + "UPLOADING" + "-"*20)
upload_batch("/home/doli/bp/BP-application/monitor/test_data")
print("-"*20 + "SEARCHING" + "-"*20 + "")
search_batch()
