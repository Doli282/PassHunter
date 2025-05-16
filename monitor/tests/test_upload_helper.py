# Generated with PyCharm IDE with feature "Generate Unit Tests" for upload_bulk_helper() function
import unittest
from unittest.mock import patch, AsyncMock, MagicMock

from monitor import upload_bulk_helper
from opensearchpy.helpers import BulkIndexError

@patch("monitor.logging")
@patch("monitor.helpers.bulk")
@patch("monitor.opensearch")
class TestUploadBulkHelper(unittest.TestCase):
    def test_no_actions(self, client, mock_helpers, mock_logging):
        """Test case when no actions are provided."""
        # Run the tested function
        upload_bulk_helper(None)

        # Assert nothing was called
        mock_helpers.assert_not_called()
        mock_logging.error.assert_not_called()

    def test_successful_upload(self, client, mock_helpers, mock_logging):
        """Test case for successful bulk upload."""
        # prepare mocks
        mock_helpers.return_value = (10, [])
        actions = [{}] * 10

        # Run the tested function
        upload_bulk_helper(actions=actions, amount=10)

        # Assert success
        mock_helpers.assert_called_once_with(
            client, actions, stats_only=True, raise_on_error=False, request_timeout=600
        )
        mock_logging.info.assert_called_once_with("Successfully uploaded 10 documents.")
        mock_logging.error.assert_not_called()

    def test_partial_success_upload(self, client, mock_helpers, mock_logging):
        """Test case for partial success during bulk upload."""
        mock_helpers.return_value = (5, [])
        actions = [{}] * 10
        upload_bulk_helper(actions=actions, amount=10)
        mock_helpers.assert_called_once_with(
            client, actions, stats_only=True, raise_on_error=False, request_timeout=600
        )
        mock_logging.error.assert_called_once_with(
            "Not all documents were indexed. Success rate: (5/10)"
        )

    def test_bulk_index_error(self, client, mock_helpers, mock_logging):
        """Test case for BulkIndexError exception during bulk upload."""
        mock_helpers.side_effect = BulkIndexError("Test error")
        actions = [{}] * 5
        upload_bulk_helper(actions=actions, amount=5)

        mock_helpers.assert_called_once_with(
            client, actions, stats_only=True, raise_on_error=False, request_timeout=600
        )
        mock_logging.error.assert_any_call("Error during bulk indexing")
        self.assertEqual(mock_logging.error.call_count, 2)