"""Extractor - extracts files from archives"""
import logging
import os
import shutil
import tempfile
from tempfile import mkdtemp

import patoolib

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
logging.basicConfig(format=LOGGING_FORMAT, level=os.getenv("LOGGING_LEVEL", "INFO"))

# Define filter for to-be-extracted files
KEYWORDS = ["pass"]

# Define paths for storing files
DOWNLOAD_PATH = "/data/downloads"
UPLOAD_PATH = "/data/uploads"

@downloader.task(name='extractor.extract_archive')
def extract_archive(archive_name: str, archive_password: str, archive_dir: str = DOWNLOAD_PATH, destination_path: str = UPLOAD_PATH, keywords: list[str] = KEYWORDS) -> str:
    """
    Extract an archive.
    The archive is extracted to a temporary directory and then moved to the destination directory.

    Args:
        archive_name (str): Name of the archive to extract.
        archive_password (str): Password for the archive.
        archive_dir (str): Directory where the archive is stored.
        destination_path (str): Directory where the extracted files should be stored.
        keywords (list[str]): List of keywords to filter files by.

    Returns:
        str: Name of the destination directory.
    """
    logging.info(f"Received request to extract '{archive_name}' with password '{archive_password}'")
    archive_path = os.path.join(archive_dir, archive_name)

    # Create a temporary directory to extract the archive to.
    with tempfile.TemporaryDirectory(ignore_cleanup_errors = True) as tmpdir:
        try:
            # Check if the archive really is a valid archive (according to the used tools).
            if not patoolib.is_archive(archive_path):
                raise ValueError(f"Archive '{archive_name}' is not a valid archive")

            # Extract the entire archive to the temporary directory
            patoolib.extract_archive(archive_path, outdir=tmpdir, verbosity=-1, interactive=False, password=archive_password)

            # Move significant files to destination directory
            destination = mkdtemp(dir=destination_path)
            print("destianation: ", destination)
            # Walk through the extracted archive and pick wanted files.
            i = 0 # Iteration variable to distinguish files with the same name.
            for root, _, files in os.walk(tmpdir):
                # Check if a file is the wanted file (contains significant keywords) and move it to destination, if yes.
                for filename in files:
                    if _filename_filter(filename, keywords):
                        try:
                            # Flatten the directory structure and rename the file.
                            dest_filename = f"{archive_name}_{i}_{filename}".replace(' ', '_')
                            shutil.move(os.path.join(root, filename), os.path.join(destination, dest_filename))
                            i += 1
                            logging.debug(f"File '{filename}' moved to '{dest_filename}'")
                        except Exception as e:
                            logging.error(f"Failed to move file '{filename}': {e}")
                            continue

            logging.debug(f"Extracted archive '{archive_name}' to '{destination}'")
            # After the extraction, send the destination of the extracted files as a task to celery queue.
            destination_name = os.path.basename(destination)
            uploader.send_task("monitor.process_batch", args=[destination_name])
            logging.info(f"Task with destination '{destination_name}' sent to celery.")

        # Catch exception caused by patoolib.
        except patoolib.util.PatoolError as e:
            logging.error(f"Failed to extract archive: {e}")
            return ""
        # Catch exceptions caused by invalid values.
        except ValueError as e:
            logging.error(f"Failed to extract archive: {e}")
            return ""
        # Catch all remaining exceptions.
        except Exception as e:
            logging.error(f"Failed to extract archive: {e}")
            return ""
        finally:
            # Cleanup
            os.remove(archive_path)

    logging.info(f"Extractor has finished.")
    return destination

def _filename_filter(filename: str, keywords: list[str]) -> bool:
    """
    Filter names of files to extract, according to a list of keywords.

    Args:
        filename (str): Name of the file to filter.
        keywords (list[str]): List of keywords to filter files by.

    Returns:
        bool: True if the file should be extracted, False otherwise.
    """
    # If no keywords are provided, always return True.
    if keywords is None:
        return True
    return  any(word.lower() in filename.lower() for word in keywords)
