# PassHunter

A cloud-based application for monitoring and searching domains across various datasets.

## Overview

PassHunter is a microservices-based application that:
- Downloads and processes datasets from Telegram channels
- Stores and indexes data using OpenSearch
- Provides a web interface for domain monitoring and search
- Sends alerts when monitored domains are found in new datasets

For detailed project specification, see [specification.txt](specification.txt).

## Prerequisites

- Podman or Docker installed
- Python 3.11 or later
- Git

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PassHunter
```

2. Install podman-compose (if using Podman):
```bash
pip install podman-compose
```

3. Create and configure the environment file:
```bash
cp .env.example .env
```
Edit the `.env` file and set the following values:
- Telegram API credentials (TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_BOT_TOKEN)
- PostgreSQL credentials (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB)
- OpenSearch admin password (OPENSEARCH_INITIAL_ADMIN_PASSWORD)
- Application secret key (SECRET_KEY)

## Starting the Application

1. Start all services using podman-compose:
```bash
podman-compose up -d
```

2. Access the services:
- Web Application: http://localhost:5000
- OpenSearch Dashboards: http://localhost:5601
- Mail Server UI: http://localhost:8025

## Service Ports

- Web Application: 5000
- OpenSearch Node 1: 9200 (API), 9600 (Performance Analyzer)
- OpenSearch Dashboards: 5601
- Mail Server: 1025 (SMTP), 8025 (Web UI)

## Stopping the Application

To stop all services:
```bash
podman-compose down
```

To stop and remove all volumes (this will delete all data):
```bash
podman-compose down -v
```

## Development

The application is built using microservices architecture. Each service has its own directory:
- `data-download/`: Telegram watcher, downloader, and archive parser
- `gui/`: Web application
- `domain-watcher/`: Domain monitoring service
- `opensearch/`: OpenSearch configuration

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Submit a pull request

## License

[Add your license information here]
