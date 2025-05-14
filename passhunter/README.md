# PassHunter - Web Application

The web GUI used for the PassHunter application.
It enables users to interact with the application.

## Features:

- one workspace per user = registered users have their own watchlists and alerts
- manage watchlists = list of monitored strings
- search for domains/passwords from GUI = query OpenSearch for the strings
- view alerts = get notified when a monitored string is found

## Installation

Make a virtual environment and install requirements from `requirements.txt`.
```shell
pip install -r requirements.txt
```

Configure variables in `.flaskenv`.
Configure secrets and environment variables:
```dotenv
# Environment secrets for the PassHunter web application
# Flask variables
SECRET_KEY=...

# Database variables
DATABASE_URL=postgresql+psycopg2://hunter_user:hunter_password@localhost:5432/hunter_db

# Mail server - error reporting
MAIL_SERVER=localhost
MAIL_PORT=8025
MAIL_USE_TLS=...
MAIL_USERNAME=...
MAIL_PASSWORD=...

# OpenSearch Configuration
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200
OPENSEARCH_USER=...
OPENSEARCH_ADMIN_PASSWORD=...
```

## Run

Run the application
```shell
python passhunter.py
```

To debug, set the environment to debug and run:
```shell
flask run
```

## Usage

The web application shall be available at http://localhost:5000

### 1. Data input

When the source channels are defined, let the daemons do their work.
In case you want to add a new channel later, put the channel ID in the Forwarder's configuration and reload the container.

### 2. GUI 

In the web GUI it is possible to use search and query the collected data.
The search option on `/search` is available to anyone.
To use an automatic monitoring, register an account first on `/register`.
(Go to `/login` and click `Register here`.)

As a registered user, you can set up watchlists on `/watchlists`.
A watchlist can be active or inactive.
That setting affects whether new alerts are raised or not.
A watchlist can have assigned an email address.
When an email address is set and email alerts are allowed (tick the checkbox) emails will be sent as a notification.
Unless both conditions are met (filled email address and checked checkbox) no emails will come.

You can have multiple watchlists.
A watchlist can contain many domains.
Domain (actually any string will do) can use wildcard syntax.
All symbols are treated as they are, except `*` for any number of characters and `?` for one character.

If a monitored domain appears in the newly downloaded dataset, an alert is raised.
A list of all alerts is visible on `/alerts`.
Alerts can be marked as registered (or deregistered again).
It is possible to show detailed information about the alert.
There is a list of lines in which the string was found.
