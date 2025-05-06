# 01_Download_file

Download a file from a new incoming message.

## Preconditions

- Telegram account
- prepared Telegram bot
  - registered bot
  - bot added in the Telegram channel
- prepared environment variables
- setup messaging queue

## Steps

1. Send a message with a file to the channel with the daemon.

## Expected Result

1. The file is downloaded to the destination specified in the configuration.
2. The messaging queue registers a message with the path to the file.
