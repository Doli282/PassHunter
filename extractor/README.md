# Extractor

Extractor extracts archives.

## Modus operandi

1. Extractor takes a message from a message queue.
2. It finds the archive on the specified path and processes it
3. Extractor extracts only selected files from the archive.
4. A message with a path to extracted files is sent to the second message queue.
5. The Original archive is removed.

Supported arhive formats:
- zip
- rar

## Installation

Make a virtual environment and install requirements from `requirements.txt`.
```shell
pip install -r requirements.txt
```

## Configuration

Configure the message queues for Celery in `celeryconfig.py`.

## Usage

Run as a Celery worker:
```shell
celery -A extractor worker --loglevel=info --queues=downloads
```
