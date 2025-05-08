"""Configuration of Celery for the Extractor."""

import os
from dotenv import load_dotenv
from kombu import Queue, Exchange
from kombu.abstract import Object

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

class ConfigUploader(Object):
    """Configuration class for uploader vhost."""
    broker_url = os.getenv("UPLOADER_BROKER_URL")

    # Declare named queues bound to direct exchanges
    task_queues = (
        Queue("uploads", Exchange("uploads", type="direct"), routing_key="uploads"),
    )

    # Route specific tasks to the appropriate queue
    task_routes = {
        "monitor.process_batch": {"queue": "uploads", "routing_key": "uploads"},
    }

    # auto-create any queue routed-to
    task_create_missing_queues = True

class ConfigDownloader(Object):
    """Configuration class for downloader vhost."""
    broker_url = os.getenv("DOWNLOADER_BROKER_URL")

    # Declare named queues bound to direct exchanges
    task_queues = (
        Queue("downloads", Exchange("downloads", type="direct"), routing_key="downloads"),
    )

    # Route specific tasks to the appropriate queue
    task_routes = {
        "extractor.extract_archive": {"queue": "downloads", "routing_key": "downloads"},
    }

    # auto-create any queue routed-to
    task_create_missing_queues = True