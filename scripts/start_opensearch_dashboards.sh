#!/bin/bash

# Source the configuration
source "$(dirname "$0")/config.sh"

# Create network if it doesn't exist
podman network create $NETWORK_NAME 2>/dev/null || true

# Stop and remove existing container if it exists
podman stop $DASHBOARDS_CONTAINER || true
podman rm $DASHBOARDS_CONTAINER || true

# Start OpenSearch Dashboards container
podman run -d \
  --name $DASHBOARDS_CONTAINER \
  --network $NETWORK_NAME \
  -p $DASHBOARDS_PORT:5601 \
  -e "OPENSEARCH_HOSTS=[\"https://$OPENSEARCH_CONTAINER:$OPENSEARCH_PORT\"]" \
  $DASHBOARDS_IMAGE

echo "OpenSearch Dashboards container started. Use 'podman logs $DASHBOARDS_CONTAINER' to view logs." 