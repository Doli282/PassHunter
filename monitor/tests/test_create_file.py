# Generated with PyCharm IDE with feature "Generate Unit Tests" for create_file() function
import unittest
from unittest.mock import patch, MagicMock

from models.file import File
from monitor import create_file


@patch("monitor.Session")
class TestCreateFile(unittest.TestCase):

    def setUp(self):
        self.filename = "example.txt"
        self.digest = b"dummyhashvalue"
        self.mock_session_instance = MagicMock()

    def test_create_file_success(self, mock_session):
        """
        Test case for successfully creating a file in the database.
        Ensures that the file is added and committed to the session.
        """

        mock_session.return_value.__enter__.return_value = self.mock_session_instance

        result = create_file(self.filename, self.digest)

        self.mock_session_instance.add.assert_called_once_with(result)
        self.mock_session_instance.commit.assert_called_once()
        self.assertIsInstance(result, File)
        self.assertEqual(result.name, self.filename)
        self.assertEqual(result.hash, self.digest)

    def test_create_file_session_commit_failure(self, mock_session):
        """
        Test case for handling session commit failure while creating a file.
        Ensures that an exception is raised and session commit is not silently ignored.
        """
        mock_session.return_value.__enter__.return_value = self.mock_session_instance
        self.mock_session_instance.commit.side_effect = Exception("Database commit failed")

        with self.assertRaises(Exception) as context:
            create_file(self.filename, self.digest)

        self.assertEqual(str(context.exception), "Database commit failed")
        self.mock_session_instance.add.assert_called_once_with(self.mock_session_instance.add.call_args[0][0])
        self.mock_session_instance.commit.assert_called_once()
