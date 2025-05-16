# TC_01_Forward

Forward new messages to the specified channel.

## Preconditions

- Telegram account
- prepared environment variables
- prepared configuration in config.py
  - defined channel IDs

## Steps

1. Send messages to the source channels
    - send messages with files
      - attach one file
      - attach multiple files in group
    - send messages without files
    - send messages to all defined source channels

## Expected Result

Messages with documents are forwarded to the destination channel.
Messages without files are not forwarded.
Messages with many documents are forwarded in multiple messages - one message per document.