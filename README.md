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

3. Prepare Telegram daemons. Register the Telegram application and obtain API ID on https://docs.telethon.dev/en/stable/basic/signing-in.html.
   1. Login on https://my.telegram.org/.
   2. Click API Development Tools.
   3. Create a new application. Fill in the details.
   4. Get API TOKEN and API HASH.
   5. For the Downloader module, register a new bot by Telegram [@BotFather](https://t.me/botfather) and get the BOT TOKEN.
   6. Add the Downloader bot to channels from which files shall be downloaded.
   7. Add channel IDs and to Forwarder's `config.py`.

4. Set up a mail server
   - E.g., when using gmail SMTP server, use gmail account and [generate password](https://myaccount.google.com/apppasswords) for the application.

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

## Stopping the Application

To stop all services:
```bash
docker compose down
```

## Testing

Tests are written in `tests/` directories across the application by each module.
