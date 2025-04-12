#!/bin/bash

# Make sure we're in the project root directory
cd "$(dirname "$0")/.."

# Create network if it doesn't exist
podman network create $NETWORK_NAME 2>/dev/null || true

# Start containers in order
echo "Starting PostgreSQL..."
./scripts/start_postgres.sh

echo "Starting OpenSearch..."
./scripts/start_opensearch.sh

#echo "Starting OpenSearch Dashboards..."
#./scripts/start_opensearch_dashboards.sh

echo "Starting Web Application..."
./scripts/start_gui.sh

echo "All containers started!"
echo "PostgreSQL: localhost:5432"
echo "OpenSearch: localhost:9200"
#echo "OpenSearch Dashboards: localhost:5601"
echo "Web Application: localhost:5000" 