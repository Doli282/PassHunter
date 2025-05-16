# Monitor

Monitor is used to upload documents into OpenSearch and run a query on the dataset for monitored domains.

## Installation

Install dependencies according to `requirements.txt`
```shell
pip install -r requirements.txt
```

## Celery

Monitor takes tasks from a message queue.
It runs as a celery worker.

Set up environment variables for Celery:
```dotenv
# Celery Configuration
UPLOADER_BROKER_URL=...
# Database Confiugration
DATABASE_URL=...
```

### Run

Before the run, read the documentation till the end for all environment variables.
To run the application, launch:
```shell
celery -A monitor worker --loglevel=info --queues=uploads
```

## OpenSearch

`Ingest attachment` plugin is used.
The plugin needs to be installed first

```shell
./bin/opensearch-plugin install ingest-attachment
```

Set up environment variables for OpenSearch:
```dotenv
# OpenSearch Configuration
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200
OPENSEARCH_USER=...
OPENSEARCH_ADMIN_PASSWORD=...
```

## Alerting

An alert is generated each time a domain on an active watchlist is detected in a new dataset.

## Email

An email is sent as a part of the alerting service.
If a user has set an email address and activated the function, an email with an alert is sent.
The email is sent using the gmail smtp.

A gmail account has to be provided.
This is feasible only when the application is used by a single user or a group of users.
For production use, a real SMTP server shall be used.

### How to set up the gmail account

1. Create a password for the application. https://myaccount.google.com/apppasswords
2. Use the password and gmail account in the monitor.py script -> provide as env variable.
3. Use gmail SMTP server for sending emails.

```dotenv
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=465
MAIL_USERNAME=...
MAIL_PASSWORD=...
EMAIL_SENDER=no-reply@passhunter.com
```

## Run tests

Tests are in the `/tests/` directory.
Run tests from the module's root directory in a virtual environment with the module's requirements.
```shell
python3 -m unittest discover tests
```
