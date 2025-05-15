import asyncio
import unittest
from time import sleep
from unittest.mock import AsyncMock, patch, MagicMock

import downloader

@patch("downloader.logging")
class TestDownload(unittest.IsolatedAsyncioTestCase):

    @patch("downloader.queue", new_callable=AsyncMock)
    async def test_handler_queue(self, mock_queue, mock_logger=None):
        """ Test the handler function - message with document"""
        # Prepare mock message
        mock_message = AsyncMock()
        mock_message.document = True

        # Run the tested function
        await downloader.handler(mock_message)

        # Assert the message was put into the queue
        mock_queue.put.assert_awaited_once_with(mock_message)

    @patch("downloader.queue", new_callable=AsyncMock)
    async def test_handler_not_queue(self, mock_queue, mock_logger=None):
        """ Test the handler function - message without document"""
        # Prepare mock message
        mock_message = AsyncMock()
        mock_message.document = False

        # Run the tested function
        await downloader.handler(mock_message)

        # Assert the message was put into the queue
        mock_queue.put.assert_not_awaited()


    @patch("downloader.Config")
    @patch("downloader.celery")
    @patch("downloader.queue.task_done", new_callable=MagicMock)
    @patch("downloader.queue.get", new_callable=AsyncMock)
    async def test_worker_password(self, mock_queue_get, mock_queue_task, mock_celery, mock_config, mock_logger = None):
        """Test worker function with a valid password in the message."""
        # Set up mocks
        mock_message = AsyncMock()
        mock_message.file.name = "test.zip"
        mock_message.raw_text = "hi\nthis is my secret:\npassword=target\nbye"
        mock_message.download_media = AsyncMock()
        mock_config.DOWNLOAD_PATH = "/tmp"
        # Make sure the loop ends after one iteration
        mock_queue_get.side_effect = [mock_message, asyncio.CancelledError]

        # Run the tested function
        task = asyncio.create_task(downloader.worker("w01"))
        await asyncio.sleep(0.05)
        task.cancel()
        await task

        # Assert the attempted download
        mock_message.download_media.assert_awaited_once_with("/tmp/test.zip")
        mock_celery.send_task.assert_called_once_with('extractor.extract_archive', args=["test.zip", "target"])
        mock_queue_task.assert_called_once()

    @patch("downloader.Config")
    @patch("downloader.celery")
    @patch("downloader.queue", new_callable=AsyncMock)
    async def test_worker_no_password(self, mock_queue, mock_celery, mock_config, mock_logger=None):
        """Test worker function with an invalid password in the message."""
        # Set up mocks
        mock_message = AsyncMock()
        mock_message.file.name = "test.zip"
        mock_message.raw_text = "hi\nthis is my secret:\npas48s541w5ord=target\nbye"
        mock_message.download_media = AsyncMock()
        mock_config.DOWNLOAD_PATH = "/tmp"
        # Make sure the loop ends after one iteration
        mock_queue.get.side_effect = [mock_message, asyncio.CancelledError]

        # Run the tested function
        task = asyncio.create_task(downloader.worker("w01"))
        await asyncio.sleep(0.05)
        task.cancel()
        await task

        # Assert the attempted download
        mock_message.download_media.assert_awaited_once_with("/tmp/test.zip")
        mock_celery.send_task.assert_called_once_with('extractor.extract_archive', args=["test.zip", ""])
        mock_queue.task_done.assert_called_once()


    @patch("downloader.client")
    @patch("downloader.Config")
    @patch("downloader.worker")
    async def test_start(self, mock_worker, mock_config, mock_client, mock_logger=None):
        """Test how Downloader handles workers"""
        # Prepare mocks
        worker_count = 2
        mock_config.WORKER_COUNT = worker_count
        mock_client.run_until_disconnected = AsyncMock()
        mock_client.disconnect = MagicMock()
        mock_worker.side_effect = asyncio.CancelledError

        # Run the tested function
        await downloader.start()

        # Assert that the correct number of workers was created
        self.assertEqual(mock_worker.call_count, worker_count)
        mock_client.run_until_disconnected.assert_awaited_once()
        mock_client.disconnect.assert_called_once()


    def test_password_extraction(self, mock_logger=None):
        """Test the regex for parsing messages for passwords."""
        pass_yes = ["'emoji' pass: PASSWORD", "password : my234strong09ipass++", "dummytext Password = qwerty"]
        pass_no = ["P@$$word: the_strong_password", "The password is 'alahomora'."]

        for password in pass_yes:
            self.assertTrue(downloader.extract_password(password))

        for password in pass_no:
            self.assertFalse(downloader.extract_password(password))