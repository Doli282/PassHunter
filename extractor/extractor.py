"""Extractor - extracts files from archives"""
import logging
import os
from tempfile import mkdtemp

import rarfile
import zipfile

from celery import Celery
from celeryconfig import ConfigUploader, ConfigDownloader

# Downloader
downloader = Celery('downloader')
downloader.config_from_object(ConfigDownloader)

# Uploader
uploader = Celery('uploader')
uploader.config_from_object(ConfigUploader)

# Set up logging
LOGGING_FORMAT = '%(asctime)s Extractor: %(levelname)s: %(message)s'
logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO)

# Define filter for to-be-extracted files
KEYWORDS = ["pass"]

@downloader.task(name='extractor.extract_archive')
def extract_archive(archive_path: str, archive_password: str) -> None:
    logging.info(f"Received request to extract '{archive_path}' with password '{archive_password}'")

    # Extract the archive into a new directory
    destination = mkdtemp()

    try:
        # Choose the extractor function based on the archive extension
        match os.path.splitext(archive_path)[-1]:
            case '.zip':
                extract_zip(archive_path, archive_password, destination)
            case '.rar':
                extract_rar(archive_path, archive_password, destination)
            case _:
                raise ValueError(f"Unsupported archive type '{os.path.splitext(archive_path)[-1]}'")
        logging.info(f"Archive extracted")
    except Exception as e:
        logging.error(f"Failed to extract archive: {e}")

    try:
        # Send a message to the uploading queue
        uploader.send_task('uploader.process_batch', args=[destination])
    except Exception as e:
        logging.error(f"Failed to send message to the uploading queue: {e}")

    # Remove the processed archive
    _clean(archive_path)
    logging.info(f"Extractor has finished.")
    return

def extract_zip(archive_path: str, archive_password:str, extract_to: str) -> None:
    """
    Extract only selected files from the zip archive.

    Args:
        archive_path (str): Path to the zip archive.
        archive_password (str): Password for the zip archive.
        extract_to (str): Directory to extract the files to.

    Returns:
        None
    """
    logging.debug("Extracting zip archive.")
    # Save the name of the archive - use it for naming the extracted files
    archive_name = os.path.splitext(archive_path)[-1]

    # Open the zip archive
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        # Iteration variable for naming
        i = 1

        # Read information on all files and filter only desired files
        for file in zip_ref.infolist():
            if _filename_filter(file.filename):
                logging.debug(f"File '{file.filename}' found, extracting")

                # Rename the file to flatten to structure
                file_filename = os.path.splitext(file.filename)[-1]
                new_filename = f"{archive_name}_{file_filename}_{i}"
                out_path = os.path.join(extract_to, new_filename)

                # Extract the file
                if zip_ref.extract(file, out_path, bytes(archive_password, 'utf-8') if archive_password else None):
                    logging.debug(f"File extracted to {out_path}")
                else:
                    logging.error(f"Failed to extract file '{file.filename}'")
                i += 1

def extract_rar(archive_path: str, archive_password:str, extract_to: str) -> bool:
    """
    Extract only selected files from the rar archive.

    Args:
        archive_path (str): Path to the rar archive.
        archive_password (str): Password for the rar archive.
        extract_to (str): Directory to extract the files to.

    Returns:
        bool: True if extraction was successful, False otherwise.
    """
    logging.debug("Extracting rar archive.")
    # Save the name of the archive - use it for naming the extracted files
    archive_name = os.path.splitext(archive_path)[-1]

    # Open the rar archive
    with rarfile.RarFile(archive_path) as rar_ref:
        # Set password if provided
        if archive_password:
            rar_ref.setpassword(archive_password)
        elif rar_ref.needs_password():
            logging.error("Password required for extraction, but no password provided.")
            return False

        # Iteration variable for naming
        i = 1

        # Read information on all files and filter only desired files
        for file in rar_ref.infolist():
            if _filename_filter(file.filename):
                logging.debug(f"File '{file.filename}' found, extracting")

                # Rename the file to flatten to structure
                file_filename = os.path.splitext(file.filename)[-1]
                new_filename = f"{archive_name}_{file_filename}_{i}"
                out_path = os.path.join(extract_to, new_filename)

                # Rewrite the file outside the archive
                with rar_ref.open(file) as source, open(out_path, 'wb') as target:
                    target.write(source.read())
                    logging.debug(f"File extracted to {out_path}")

                i += 1

    return True

def _filename_filter(filename: str) -> bool:
    """
    Filter names of files to extract, according to a list of keywords.

    Args:
        filename (str): Name of the file to filter.

    Returns:
        bool: True if the file should be extracted, False otherwise.
    """
    return  any(word.lower() in filename.lower() for word in KEYWORDS)

def _clean(archive: str):
    """
    Clean after extraction.

    Args:
        archive (str): Path to the archive.

    Returns:
        None
    """
    os.remove(archive)
    logging.debug("Archived removed.")
