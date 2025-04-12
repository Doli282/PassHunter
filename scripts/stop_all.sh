#!/bin/bash

# Source the configuration
source "$(dirname "$0")/config.sh"

echo "Stopping all application containers..."

# Stop GUI container
echo "Stopping GUI container..."
podman stop $WEB_APP_CONTAINER

# Stop OpenSearch container
echo "Stopping OpenSearch container..."
podman stop $OPENSEARCH_CONTAINER

# Stop OpenSearch Dashboards container
echo "Stopping OpenSearch Dashboards container..."
podman stop $DASHBOARDS_CONTAINER

# Stop PostgreSQL container
echo "Stopping PostgreSQL container..."
podman stop $POSTGRES_CONTAINER

echo "All containers stopped."


if [[ -n $1 ]]; then
    echo "Removing containers..."
    podman rm $WEB_APP_CONTAINER
    podman rm $OPENSEARCH_CONTAINER
    podman rm $DASHBOARDS_CONTAINER
    podman rm $POSTGRES_CONTAINER
    echo "All containers removed."
    if [[ -n $2 ]]; then
        echo "Removing networks and volumes..."
        podman network rm $NETWORK_NAME
        podman volume rm $POSTGRES_VOLUME
        podman volume rm $OPENSEARCH_VOLUME
        podman volume rm $WEB_APP_VOLUME
        echo "Network and volumes removes."
    fi
fi