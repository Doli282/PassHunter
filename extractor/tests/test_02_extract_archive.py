"""Test the extract_archive function. - TC_02"""
import unittest
import zipfile
from unittest import mock
import os
import tempfile
import shutil

# Import the tested module
import extractor

class TestExtractor(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for downloads and uploads.
        self.download_dir = tempfile.mkdtemp()
        self.upload_dir = tempfile.mkdtemp()
        self.archive_name = 'test_archive.zip'
        self.archive_path = os.path.join(self.download_dir, self.archive_name)

        # Create a dummy archive file.
        with zipfile.ZipFile(self.archive_path, 'w') as zip_file:
            zip_file.writestr('pass_file.txt', 'Dummy password file')
            zip_file.writestr('other_file.txt', 'Dummy other file')

    def tearDown(self):
        # Remove temporary directories
        shutil.rmtree(self.download_dir)
        shutil.rmtree(self.upload_dir)

    @mock.patch('extractor.uploader.send_task')
    def test_extract_archive(self, mock_send_task):
        """Test the extract_archive function with dummy data."""
        # Run the tested function
        destination = extractor.extract_archive(
            archive_name=self.archive_name,
            archive_password='',
            archive_dir=self.download_dir,
            destination_path=self.upload_dir,
            keywords=['pass']
        )

        # Check that send_task was called.
        mock_send_task.assert_called_once()

        # Check the file was extracted
        self.assertTrue(os.path.exists(os.path.join(destination, 'test_archive.zip_0_pass_file.txt')))


    @mock.patch('extractor.os.remove')
    @mock.patch('extractor.uploader.send_task')
    @mock.patch('extractor.shutil.move')
    @mock.patch('extractor.os.walk')
    @mock.patch('extractor.patoolib.extract_archive')
    @mock.patch('extractor.patoolib.is_archive', return_value=True)
    def test_extract_archive_mock(self, mock_is_archive, mock_extract_archive, mock_os_walk, mock_shutil_move, mock_send_task, mock_os_remove):
        """Run the extract_archive function with mocks."""
        # Mock os.walk to simulate extracted files.
        mock_os_walk.return_value = [
            (self.download_dir, [], ['pass_file.txt', 'other_file.txt'])
        ]

        # Call the extract_archive function.
        extractor.extract_archive(
            archive_name=self.archive_name,
            archive_password='password',
            archive_dir=self.download_dir,
            destination_path=self.upload_dir,
            keywords=['pass']
        )
        # Check that is_archive was called.
        mock_is_archive.assert_called_once()

        # Check that extract_archive was called.
        mock_extract_archive.assert_called_once()

        # Check that shutil.move was called only for the file matching the keyword.
        mock_shutil_move.assert_called_once()
        args, kwargs = mock_shutil_move.call_args
        self.assertIn('pass_file.txt', args[0])

        # Check that send_task was called.
        mock_send_task.assert_called_once()

        # Check that os.remove was called.
        mock_os_remove.assert_called_once()
        mock_os_remove.assert_called_with(self.archive_path)

    @mock.patch('extractor.os.remove')
    @mock.patch('extractor.logging.error')
    @mock.patch('extractor.patoolib.extract_archive')
    @mock.patch('extractor.patoolib.is_archive', return_value=False)
    def test_extract_archive_invalid_archive(self, mock_is_archive, mock_extract_archive, mock_logging_error, mock_os_remove):
        """Run the extract_archive function with mocks."""
        # Call the extract_archive function with an invalid archive
        extractor.extract_archive(
            archive_name=self.archive_name,
            archive_password='password',
            archive_dir=self.download_dir,
            destination_path=self.upload_dir,
            keywords=['pass']
        )

        # Check that is_archive was called.
        mock_is_archive.assert_called_once()

        # Check that extract_archive was not called.
        mock_extract_archive.assert_not_called()

        # Check that an error was logged
        mock_logging_error.assert_called()

        # Check that os.remove was called.
        mock_os_remove.assert_called_once()
        mock_os_remove.assert_called_with(self.archive_path)
