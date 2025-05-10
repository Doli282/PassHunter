"""Extractor - extracts files from archives"""
import logging
import os
from tempfile import mkdtemp

import patoolib
import rarfile
import zipfile
import py7zr

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
logging.basicConfig(format=LOGGING_FORMAT, level=logging.DEBUG)

# Define filter for to-be-extracted files
KEYWORDS = ["pass"]

# Define paths for storing files
DOWNLOAD_PATH = "/tmp/downloads"
UPLOAD_PATH = "/tmp/uploads"

@downloader.task(name='extractor.extract_archive')
def extract_archive(archive_name: str, archive_password: str) -> None:
    logging.info(f"Received request to extract '{archive_name}' with password '{archive_password}'")
    archive_path = os.path.join(DOWNLOAD_PATH, archive_name)

    # Extract the archive into a new directory
    destination = mkdtemp(dir=UPLOAD_PATH)
    logging.debug(f"Extracting archive to '{destination}'")

    try:
        # Choose the extractor function based on the archive extension
        logging.debug(f"Archive extension: {os.path.splitext(archive_name)[-1]}")
        match os.path.splitext(archive_name)[-1]:
            case '.zip':
                extract_zip(archive_path, archive_password, destination)
            case '.rar':
                extract_rar(archive_path, archive_password, destination)
            case _:
                raise ValueError(f"Unsupported archive type '{archive_name}'")
        logging.info(f"Archive extracted")
    except Exception as e:
        logging.error(f"Failed to extract archive: {e}")

    try:
        # Send a message to the uploading queue
        uploader.send_task('uploader.process_batch', args=[os.path.basename(destination)])
    except Exception as e:
        logging.error(f"Failed to send message to the uploading queue: {e}")

    # Remove the processed archive
    #os.remove(archive_name)
    logging.info(f"Extractor has finished.")
    return

def extract_patool(archive_path: str, archive_password:str, extract_to: str) -> None:
    logging.debug("Extracting patool archive.")
    patoolib.extract_archive(archive_path, verbosity=1, outdir=extract_to, interactive=False, password=archive_password)

def extract_7z(archive_path: str, archive_password:str, extract_to: str) -> None:
    logging.debug("Extracting 7z archive.")
    with py7zr.SevenZipFile(archive_path, mode='r', password=archive_password) as archive:
        all_files = archive.getnames()
        selected_files = [f for f in all_files if
                          _filename_filter(f)] if KEYWORDS else None
        archive.extract(path=extract_to, targets=selected_files)

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
    archive_name = os.path.basename(archive_path)
    logging.debug(f"Archive name: {archive_name}")

    # Open the zip archive
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        # Iteration variable for naming
        i = 1
        logging.debug(f"extracting iteration = {i}")

        # Read information on all files and filter only desired files
        for file in zip_ref.infolist():
            logging.debug(f"file = {file.filename}")
            if _filename_filter(file.filename):
                try:
                    logging.debug(f"File '{file.filename}' found, extracting")

                    # Rename the file to flatten to structure
                    file.filename = f"{archive_name}_{os.path.basename(file.filename)}_{i}"
                    logging.debug(f"file.filename = {file.filename}")
                    # Extract the file
                    if zip_ref.extract(file, extract_to, bytes(archive_password, 'utf-8') if archive_password else None):
                        logging.debug(f"File '{file.filename}' extracted to {extract_to}")
                    else:
                        logging.error(f"Failed to extract file '{file.filename}'")
                    i += 1
                except zipfile.BadZipFile as e:
                    logging.error(f"Bad zip file: {e}")
                except RuntimeError as e:
                    logging.error(f"Runtime error (Problem with encryption?): {e}")
                except Exception as e:
                    logging.error(f"Unknown error: {e}")

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
    archive_name = os.path.basename(archive_path)

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
                file_filename = os.path.basename(file.filename)
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

if __name__ == "__main__":
    logging.info("Extractor started.")
    archive = "/tmp/downloads/RSLC MIX logs [PUBLIC] 114count.zip"
    extract_archive("RSLC MIX logs [PUBLIC] 114count.zip",'https://t.me/RedLineStealerLogsCloud')
    print('-'*10 + 'test archive' + '-'*10)
    #patoolib.test_archive(archive)
    print('-'*10 + 'archive format' + '-'*10)
    print(patoolib.get_archive_format(archive))
    print('-'*10 + 'formats' + '-'*10)
    #patoolib.list_formats()
    print('-'*10 + 'supported formats' + '-'*10)
    #print(patoolib.supported_formats())
    #extract_patool("/tmp/downloads/RSLC MIX logs [PUBLIC] 114count.zip",'https://t.me/RedLineStealerLogsCloud', '/tmp/uploads/')
