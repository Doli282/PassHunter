# Extractor

Extractor extracts archives.

## Modus operandi

1. Extractor takes a message from a message queue.
2. It finds the archive on the specified path and processes it
3. Extractor extracts only selected files from the archive.
4. A message with a path to extracted files is sent to the second message queue.
5. The Original archive is removed.

## Installation

Install tools used by `patool` for extraction:
```shell
apt install unrar
apt install p7zip-full
apt install file
# Add other tools as needed
```

Make a virtual environment and install requirements from `requirements.txt`.
```shell
pip install -r requirements.txt

# or install individual packages:
pip install patool
pip install celery
pip install python-dotenv
pip install pytest
```

## Configuration

Configure the message queues for Celery in `celeryconfig.py`.

Set environment variables:
```dotenv
UPLOADER_BROKER_URL=...
DOWNLOADER_BROKER_URL=...
```

## Usage

Run as a Celery worker:
```shell
celery -A extractor worker --loglevel=info --queues=downloads
```

## Testing

Test scenarios are described in the /test/ directory.

Run a pytest from the module root directory with the required packages installed:
```shell
venv-extractor/bin/pytest 
```
