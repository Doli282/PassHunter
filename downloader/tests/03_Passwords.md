# 03_Passwords

Test passwords in the messages.

## Preconditions

- Telegram account
- prepared Telegram bot
  - registered bot
  - bot added in the Telegram channel
- prepared environment variables
- setup messaging queue

## Steps

Send messages with files to the monitored channel and alter the body of the message.
The message may contain another text as well.
1. Send messages with passwords in the following formats:
   - `'emoji' pass: PASSWORD`
   - `password : my234strong09ipass++`
   - `dummytext Password = qwerty`
2. Send messages with passwords in the other formats:
   - `P@$$word: the_strong_password`
   - `The password is 'alahomora'.`
   - ...
3. Send a message without a password.

## Expected Result

1. Formats from the first batch are accepted and sent in the message to the messaging queue.
   -  Extracted passwords are: `PASSWORD`, `my234strong09ipass++`, `qwerty`
2. No passwords are extracted from the second batch. In the message to the messaging queue, an empty string is sent instead of the password
3. There is no password in the message, an empty string is sent.
