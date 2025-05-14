"""Test the forward function. - TC_01"""
import unittest
from unittest.mock import AsyncMock

from forwarder import forward
from forwarder import Config

class TestForward(unittest.IsolatedAsyncioTestCase):

    async def test_forward(self):
        """Test that a message with a document is forwarded."""
        # Create a moc message.
        mock_message = AsyncMock()
        mock_message.document = True
        mock_message.file.name = 'test.txt'
        mock_message.to_id = 123

        # Run the tested function.
        await forward(mock_message)

        # Assert the forwarding was called on the message.
        mock_message.forward_to.assert_awaited_once_with(int(Config.TARGET_CHANNEL_ID))

    async def test_not_forward(self):
        """Test that a message without a document is not forwarded."""
        # Create a moc message.
        mock_message = AsyncMock()
        mock_message.document = False
        mock_message.file.name = 'test.txt'
        mock_message.to_id = 123

        # Run the tested function.
        await forward(mock_message)

        # Assert the forwarding was not called on the message.
        mock_message.forward_to.assert_not_awaited()
