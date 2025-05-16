# Generated with PyCharm IDE with the feature "Generate Unit Tests" for check_hash_in_db() function
import unittest
from unittest.mock import patch, MagicMock

from models.file import File
from monitor import check_hash_in_db


@patch("monitor.Session")
@patch("builtins.open", create=True)
class TestCheckHashInDb(unittest.TestCase):
    def setUp(self):
        self.mock_file_path = "test_file.txt"
        self.mock_digest = b"mockhashvalue"

    def test_hash_found_in_db(self, mock_open, mock_session):
        """
        Test case where the file's hash is found in the database.
        Ensures that the function returns True and the hash.
        """
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session_instance.scalar.return_value = File(hash=self.mock_digest, name="test_file.txt")

        mock_file = MagicMock()
        mock_file.read.return_value = b"mockdata"
        mock_open.return_value.__enter__.return_value = mock_file

        with patch("hashlib.file_digest", return_value=MagicMock(digest=lambda: self.mock_digest)):
            result = check_hash_in_db(self.mock_file_path)

        self.assertTrue(result[0])
        self.assertEqual(result[1], self.mock_digest)

    def test_hash_not_in_db(self, mock_open, mock_session):
        """
        Test case where the file's hash is not found in the database.
        Ensures that the function returns False and the hash.
        """
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance
        mock_session_instance.scalar.return_value = None

        mock_file = MagicMock()
        mock_file.read.return_value = b"mockdata"
        mock_open.return_value.__enter__.return_value = mock_file

        with patch("hashlib.file_digest", return_value=MagicMock(digest=lambda: self.mock_digest)):
            result = check_hash_in_db(self.mock_file_path)

        self.assertFalse(result[0])
        self.assertEqual(result[1], self.mock_digest)

    def test_hash_calculation_failed(self, mock_open, mock_session):
        """
        Test case where the hash cannot be calculated.
        Ensures that the function returns True and None.
        """
        mock_file = MagicMock()
        mock_file.read.return_value = b""
        mock_open.return_value.__enter__.return_value = mock_file

        with patch("hashlib.file_digest", return_value=MagicMock(digest=lambda: None)):
            result = check_hash_in_db(self.mock_file_path)

        self.assertTrue(result[0])
        self.assertIsNone(result[1])
