# 02_Empty_message

Send a message without a file. The downloader ignores such files.

## Preconditions

- Telegram account
- prepared Telegram bot
  - registered bot
  - bot added in the Telegram channel
- prepared environment variables
- setup messaging queue

## Steps

1. Send a message without a file to the channel with the daemon.

## Expected Result

The daemon registers a new message arrives.
As the message does not contain a downloadable file, there is no follow-up action from the daemon.
