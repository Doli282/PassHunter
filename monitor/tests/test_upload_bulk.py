import unittest
from unittest.mock import patch

#with patch('monitor.opensearch.opensearch.Client', autospec=True) as mock_client:
#    mock_client.return_value.indices.exists.return_value = True


@patch("monitor.opensearch.Client")
class MyTestCase(unittest.TestCase):
#    def setUpClass(cls):
#        cls.client_patcher = patch('monitor.opensearch.opensearch.Client', autospec=True)
#        mock_client_class = cls.client_patcher.start()
#        mock_client_class.return_value.indices.exists.return_value = True
#
#    def tearDownClass(cls):
#        cls.client_patcher.stop()
#
#    def setUp(self):
#        self.directory_path = "test_directory"
#        self.upload_time = "2025-01-01T12:00:00Z"
#        self.files = ["test1.txt", "test2.txt", "test3.txt"]

    @patch("monitor.os.path.join", return_value="joined_path")
    @patch("monitor.check_hash_in_db")
    @patch("monitor.os.listdir")
    @patch("monitor.upload_bulk_helper")
    @patch("monitor.logging")
    def test_empty_dir(self, mock_logging, mock_bulk_helper, mock_listdir, *args):
        """Test upload of empty directory."""
        # Prepare mocks
        mock_listdir.return_value = []
        from monitor import upload_bulk
        # Run the tested function
        upload_bulk(self.directory_path, self.upload_time)

        # Asserts
        mock_listdir.assert_called_once_with(self.directory_path)
        mock_bulk_helper.assert_called_once_with([], 0)

#    def test_file_exists(self, client, mock_logging, mock_bulk_helper, mock_listdir, mock_check_hash, mock_path_join, *args):
#        """Test upload of an existing file."""
#        # Prepare mocks
#        mock_listdir.return_value = self.files
#        mock_check_hash.return_value = (True, b"hash")
#
#        # Run the tested function
#        upload_bulk(self.directory_path, self.upload_time)
#
#        # Asserts
#        mock_listdir.assert_called_once_with(self.directory_path)
#        mock_check_hash.assert_called_once_with("joined_path")
#        mock_logging.debug.assert_called_once()
#        mock_bulk_helper.assert_not_called()

if __name__ == '__main__':
    unittest.main()
