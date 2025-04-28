"""Run the main application."""
from celery import Celery
from celeryconfig import ConfigUploader, ConfigDownloader

# Downloader
downloader = Celery('downloader')
downloader.config_from_object(ConfigDownloader)

# Uploader
uploader = Celery('uploader')
uploader.config_from_object(ConfigUploader)

@downloader.task(name='extractor.extract_archive')
def extract_archive(path: str) -> None:
    print(f"extracting '{path}'....")
    return