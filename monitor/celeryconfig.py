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

    imports = (
        "uploader.tasks",
    )

    # Declare named queues bound to direct exchanges
    task_queues = (
        Queue("uploads", Exchange("uploads", type="direct"), routing_key="uploads"),
    )

    # Route specific tasks to the appropriate queue
    task_routes = {
        "uploader.process_batch": {"queue": "uploads", "routing_key": "uploads"},
    }

    # auto-create any queue routed-to
    task_create_missing_queues = True
