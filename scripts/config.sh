#!/bin/bash

# Load env variables
source "$(dirname "$0")/load_env.sh"

# Container names
POSTGRES_CONTAINER="passhunter-postgres"
OPENSEARCH_CONTAINER="passhunter-opensearch"
DASHBOARDS_CONTAINER="passhunter-dashboards"
WEB_APP_CONTAINER="passhunter-web-app"

# Network name
NETWORK_NAME="passhunter-network"

# Ports
POSTGRES_PORT=5432
OPENSEARCH_PORT=9200
OPENSEARCH_ANALYZER_PORT=9600
DASHBOARDS_PORT=5601
WEB_APP_PORT=5000

# Image names
POSTGRES_IMAGE="docker.io/library/postgres:latest"
OPENSEARCH_IMAGE="docker.io/opensearchproject/opensearch:latest"
DASHBOARDS_IMAGE="docker.io/opensearchproject/opensearch-dashboards:latest"
WEB_APP_IMAGE="passhunter-web-app"

# Volume names
POSTGRES_VOLUME="postgres_data"
OPENSEARCH_VOLUME="opensearch_data" 
WEB_APP_VOLUME="web_app_data"