# PassHunter

A container-based application for monitoring domains and other strings for their occurrence in datasets circulating among threat actors.

## Overview

PassHunter is a microservices-based application that:
- Downloads and processes datasets from Telegram channels
- Stores and indexes data using OpenSearch
- Provides a web interface for watchlist management and manual search
- Sends alerts when monitored domains are found in new datasets

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Doli282/BP-application.git
cd BP-application
```

2. Install `docker` - Follow [official manual](https://docs.docker.com/engine/install/)

3. Prepare Telegram daemons. Register the Telegram application and obtain API ID based on https://docs.telethon.dev/en/stable/basic/signing-in.html.
   1. Login on https://my.telegram.org/.
   2. Click API Development Tools.
   3. Create a new application. Fill in the details.
   4. Get API TOKEN and API HASH.
   5. For the Downloader module, register a new bot by Telegram [@BotFather](https://t.me/botfather) and get the BOT TOKEN.
   6. Add the Downloader bot to channels from which files shall be downloaded.
   7. Add channel IDs and to Forwarder's `config.py`.

4. Set up a mail server
   - E.g., when using Gmail SMTP server, use gmail account and [generate password](https://myaccount.google.com/apppasswords) for the application.

5. Create and configure the environment file. Edit the `.env` file with your secrets.
```bash
cp .env.example .env
```

## Starting the Application

1. Start all services using `docker compose`:
```bash
docker compose up -d
```

2. Check that all services are running
```bash
docker compose ps -a
```

3. Access the services:
- Web Application: http://localhost:5000


## Usage

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

## Stopping the Application

To stop all services:
```bash
docker compose down
```

## Testing

Tests are written in `tests/` directories across the application by each module.
