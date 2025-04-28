"""Handling files - archive extracting, iterating, removing"""
import os
import zipfile
from os import PathLike
from pathlib import Path
from typing import IO

from app.exception.custom_exception import ZipArchiveEncrypted
from config import TEMP_FOLDER, TEMP_FILE_SUFFIX

def extract_zip(zip_file_path: str|PathLike[str]|IO[bytes],
                files_to_extract: str|tuple[str, ...] = "All Passwords.txt",
                password: str|None = None,
                extract_to: str|PathLike[str] = TEMP_FOLDER):
    """
    Extract specific files from zip archive. Can be encrypted with ZipCrypto.

    :param zip_file_path: path to zip file
    :param files_to_extract: filenames to extract
    :param password: password to the zip archive
    :param extract_to: directory to extract to

    :return: None
    """
    # Check validity of the file
    if zip_file_path is None :
        raise ValueError("zip_file_path cannot be None")
    if isinstance(zip_file_path, PathLike) and not Path(zip_file_path).exists():
        raise FileNotFoundError("zip_file_path does not exist")
    if not zipfile.is_zipfile(zip_file_path):
        raise TypeError("Provided file is not a zip file")

    # Ensure destination directory exists
    if not os.path.exists(extract_to):
        os.makedirs(extract_to, exist_ok=True)

    # Extraction of single files inspired by
    # DHARMKAR, Rajendra. How to extract all the .txt files from a zip file using Python? Online.
    # TUTORIALS POINT. Tutorials Point. 2023-08-22. Dostupné z:
    # https://www.tutorialspoint.com/how-to-extract-all-the-txt-files-from-a-zip-file-using-python.
    # [cit. 2025-01-12].
    # Open the zip archive
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        # Read info on all files
        i = 1
        for file in zip_file.infolist():
            # Filter only wanted files
            if file.filename.endswith(files_to_extract):
                try:
                    # Rename the file to flatten the structure
                    file.filename = "p_"+str(i)+TEMP_FILE_SUFFIX
                    # Extract the file
                    zip_file.extract(file, extract_to,
                                     bytes(password, 'utf-8') if password else None)
                    i += 1
                except zipfile.BadZipFile as e:
                    raise TypeError("Problems with the archive.") from e
                except RuntimeError as e:
                    raise ZipArchiveEncrypted("Zip archive encrypted, "
                                              "missing correct key not provided.") from e


# Function created by Perplexity.ai (https://www.perplexity.ai/) 2025-01-11, adjusted by me
# Prompt: "I want to delete all files in a directory from inside a python script"
def clean_directory(directory:str|PathLike[str] = TEMP_FOLDER):
    """
    Clean directory and remove all files ending with our suffix.

    :param directory: directory to clean

    :return: None
    """
    # Check if it is a directory
    if not os.path.isdir(directory):
        raise TypeError("Provided directory is not a directory")

    # Remove all files inside the directory
    for filename in os.listdir(directory):
        if filename.endswith(TEMP_FILE_SUFFIX):
            os.remove(os.path.join(directory, filename))
