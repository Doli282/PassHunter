# Generated with PyCharm IDE with the feature "Generate Unit Tests" for search_batch() function
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from monitor import search_batch


@patch("monitor.Session")
@patch("monitor.logging")
@patch("monitor.select")
class TestSearchBatch(unittest.TestCase):
    def setUp(self):
        # Set up a sample upload datetime for testing
        self.uploaded_at = datetime(2023, 10, 31, 10, 30, 0)

    def test_search_batch_logging(self, mock_select, mock_logging, mock_session):
        """
        Test that logging is performed correctly in search_batch.
        """
        # Mock the database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock the database query returning no domains
        mock_select.return_value.filter.return_value = MagicMock()
        mock_session_instance.scalars.return_value.all.return_value = []

        # Call the function under test
        search_batch(self.uploaded_at)

        # Assert logging.debug was called with the correct message
        mock_logging.debug.assert_called_with(f"Searching through the batch uploaded at {self.uploaded_at.isoformat()}")

    def test_search_batch_no_domains(self, mock_select, mock_logging, mock_session):
        """
        Test that search_batch handles the case where no domains are found.
        """
        # Mock the database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock the query to return no domains
        mock_select.return_value.filter.return_value = MagicMock()
        mock_session_instance.scalars.return_value.all.return_value = []

        # Call the function under test
        search_batch(self.uploaded_at)

        # Assert that scalar was called but no commits were made
        mock_session_instance.scalars.assert_called_once()
        mock_session_instance.commit.assert_not_called()

    def test_search_batch_domains_found(self, mock_select, mock_logging, mock_session):
        """
        Test that search_batch processes found domains correctly.
        """
        # Mock a domain returned by the query
        mock_domain = MagicMock()
        mock_domain.name = "example.com"

        # Mock the database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock the query to return a list with one domain
        mock_select.return_value.filter.return_value = MagicMock()
        mock_session_instance.scalars.return_value.all.return_value = [mock_domain]

        # Patch dependent functions `search_for_domain` and `make_alerts`
        with patch("monitor.search_for_domain") as mock_search_for_domain, \
                patch("monitor.make_alerts") as mock_make_alerts:
            # Mock the response of `search_for_domain`
            mock_search_for_domain.return_value = (1, {"file1": ["highlight1"]})

            # Call the function under test
            search_batch(self.uploaded_at)

            # Assert `search_for_domain` was called with the correct arguments
            mock_search_for_domain.assert_called_once_with(mock_domain, self.uploaded_at)

            # Assert `make_alerts` was called with the correct arguments
            mock_make_alerts.assert_called_once_with(mock_domain, self.uploaded_at, {"file1": ["highlight1"]},
                                                     mock_session_instance)

    def test_search_batch_error_handling(self, mock_select, mock_logging, mock_session):
        """
        Test that search_batch handles errors during domain processing.
        """
        # Mock a domain that will trigger an error
        mock_domain = MagicMock()
        mock_domain.name = "error.com"

        # Mock the database session
        mock_session_instance = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_session_instance

        # Mock the query to return a list with one domain
        mock_select.return_value.filter.return_value = MagicMock()
        mock_session_instance.scalars.return_value.all.return_value = [mock_domain]

        # Patch `search_for_domain` to raise an exception
        with patch("monitor.search_for_domain") as mock_search_for_domain:
            mock_search_for_domain.side_effect = Exception("Test error")

            # Call the function under test
            search_batch(self.uploaded_at)

            # Assert logging.error was called with the correct error message
            mock_logging.error.assert_called_with("Error searching for domain 'error.com': Test error")
