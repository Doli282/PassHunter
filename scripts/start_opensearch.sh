#!/bin/bash

# Source the configuration
source "$(dirname "$0")/config.sh"

# Create network if it doesn't exist
podman network create $NETWORK_NAME 2>/dev/null || true

# Stop and remove existing container if it exists
podman stop $OPENSEARCH_CONTAINER || true
podman rm $OPENSEARCH_CONTAINER || true

# Start OpenSearch container
podman run -d \
  --name $OPENSEARCH_CONTAINER \
  --network $NETWORK_NAME \
  -p $OPENSEARCH_PORT:9200 \
  -p $OPENSEARCH_ANALYZER_PORT:9600 \
  -e "discovery.type=single-node" \
  -e "OPENSEARCH_INITIAL_ADMIN_PASSWORD=${OPENSEARCH_PASSWORD}" \
  -v $OPENSEARCH_VOLUME:/usr/share/opensearch/data \
  $OPENSEARCH_IMAGE

#  -e "bootstrap.memory_lock=false" \
#  -e "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m" \

echo "OpenSearch container started. Use 'podman logs $OPENSEARCH_CONTAINER' to view logs." 