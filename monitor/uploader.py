"""Uploader - uploading files to OpenSearch """

import logging

from celery import Celery
from celeryconfig import ConfigUploader

# Celery - Uploader
uploader = Celery('uploader')
uploader.config_from_object(ConfigUploader)

# Set up logging
LOGGING_FORMAT = '%(asctime)s Extractor: %(levelname)s: %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)

@uploader.task(name='uploader.upload_batch')
def upload_batch(folder_path: str):
    pass

def upload_file(file_path: str):
    pass
