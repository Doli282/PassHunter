"""Test the forward function. - TC_01"""
import unittest
from unittest.mock import AsyncMock

from forwarder import forward
from forwarder import Config

class TestForward(unittest.IsolatedAsyncioTestCase):

    async def test_forward(self):
        """Test the forward function."""
        # Create a moc message.
        mock_message = AsyncMock()
        mock_message.document = True
        mock_message.file.name = 'test.txt'
        mock_message.to_id = 123

        # Run the tested function.
        await forward(mock_message)

        # Assert the forwarding was called on the message.
        mock_message.forward_to.assert_called_once_with(int(Config.TARGET_CHANNEL_ID))
