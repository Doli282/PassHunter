# Generated with PyCharm IDE with the feature "Generate Unit Tests" for make_alerts() function

import datetime
import unittest
from unittest.mock import MagicMock, patch

from monitor import make_alerts
from sqlalchemy.orm import Session


class TestMakeAlerts(unittest.TestCase):
    def setUp(self):
        # Preparation phase: Set up the mocks and initial test data
        self.mock_session = MagicMock(spec=Session)
        self.domain = MagicMock()
        self.domain.name = "example.com"
        self.domain.watchlists = []
        self.created_at = datetime.datetime(2023, 1, 1, 12, 0)
        self.content = {"key": ["value1", "value2"]}

    def test_make_alerts_no_watchlists(self):
        """
        Test make_alerts when the domain has no watchlists.
        """
        # Test phase: Call the function to test
        make_alerts(self.domain, self.created_at, self.content, self.mock_session)

        # Evaluation phase: Assert expected behavior
        self.mock_session.add.assert_not_called()
        self.mock_session.commit.assert_not_called()

    def test_make_alerts_inactive_watchlist(self):
        """
        Test make_alerts where the domain's watchlist is inactive.
        """
        # Preparation phase: Add an inactive watchlist to the domain
        inactive_watchlist = MagicMock()
        inactive_watchlist.is_active = False
        self.domain.watchlists.append(inactive_watchlist)

        # Test phase: Call the function to test
        make_alerts(self.domain, self.created_at, self.content, self.mock_session)

        # Evaluation phase: Assert no alerts were created or committed
        self.mock_session.add.assert_not_called()
        self.mock_session.commit.assert_not_called()

    @patch("monitor.send_email")
    def test_make_alerts_active_watchlist(self, mock_send_email):
        """
        Test make_alerts where the domain's watchlist is active.
        """
        # Preparation phase: Add an active watchlist to the domain
        active_watchlist = MagicMock()
        active_watchlist.is_active = True
        active_watchlist.send_alerts = False
        self.domain.watchlists.append(active_watchlist)

        # Test phase: Call the function to test
        make_alerts(self.domain, self.created_at, self.content, self.mock_session)

        # Evaluation phase: Assert that an alert was created and committed
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
        mock_send_email.assert_not_called()

    @patch("monitor.send_email")
    def test_make_alerts_send_email(self, mock_send_email):
        """
        Test make_alerts where alerts also send emails.
        """
        # Preparation phase: Add an active watchlist with email alerting enabled
        active_watchlist = MagicMock()
        active_watchlist.is_active = True
        active_watchlist.send_alerts = True
        active_watchlist.email = "test@example.com"
        active_watchlist.name = "Test Watchlist"
        self.domain.watchlists.append(active_watchlist)

        # Test phase: Call the function to test
        make_alerts(self.domain, self.created_at, self.content, self.mock_session)

        # Evaluation phase: Assert that an alert was created, committed, and an email was sent
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
        mock_send_email.assert_called_once_with(
            "test@example.com",
            self.domain.name,
            active_watchlist.name,
            self.created_at.strftime("%Y-%m-%d %H:%M UTC"),
        )

    @patch("monitor.send_email")
    def test_make_lert_no_email_address(self, mock_send_email):
        active_watchlist = MagicMock()
        active_watchlist.is_active = True
        active_watchlist.send_alerts = True
        active_watchlist.email = ""
        active_watchlist.name = "Test Watchlist"
        self.domain.watchlists.append(active_watchlist)

        # Run the test function
        make_alerts(self.domain, self.created_at, self.content, self.mock_session)

        # Assert alert is created, but email is not sent
        self.mock_session.add.assert_called_once()
        self.mock_session.commit.assert_called_once()
        mock_send_email.assert_not_called()
