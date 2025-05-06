from unittest import TestCase
from unittest.mock import AsyncMock, patch

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from forwarder import forward
from forwarder import Config

class TestForward(TestCase):

    @patch('forwarder.forward.TelegramClient')
    def test_forward(self, mock_client):
        mock_message = AsyncMock()
        mock_message.document = True
        mock_message.file.name = 'test.txt'
        mock_message.to_id = 123
        forward(mock_message)

        mock_message.forward_to.assert_called_once_with(int(Config.TARGET_CHANNEL_ID))

