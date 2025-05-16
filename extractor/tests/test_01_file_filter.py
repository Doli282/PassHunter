"""Test the file_filter function. - TC_01"""
import pytest

# Import the tested module
from extractor import _filename_filter

@pytest.fixture(scope='session')
def keywords():
    """Define the keywords to filter the files."""
    return ['pass']

@pytest.mark.parametrize('filename', ['All Passwords.txt', 'passwords.txt', 'passport.pdf', 'my_pass.txt'])
def test_filename_filter_success(filename: str, keywords: list[str]) -> None:
    """
    Test the filename filter function - test success.

    Args:
        filename (str): Name of the file to filter.
        keywords (list[str]): List of keywords to filter files by.

    Returns:
        None
    """
    assert _filename_filter(filename, keywords) is True

@pytest.mark.parametrize('filename', ['paswords.txt', 'document.docx', 'image.png', 'Brute.txt', 'History.txt'])
def test_filename_filter_failure(filename: str, keywords: list[str]) -> None:
    """
    Test the filename filter function - test failure.

    Args:
        filename (str): Name of the file to filter.
        keywords (list[str]): List of keywords to filter files by.

    Returns:
        None
    """
    assert _filename_filter(filename, keywords) is False
