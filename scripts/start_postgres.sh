#!/bin/bash

# Source the configuration
source "$(dirname "$0")/config.sh"

# Create network if it doesn't exist
podman network create $NETWORK_NAME 2>/dev/null || true

# Stop and remove existing container if it exists
podman stop $POSTGRES_CONTAINER || true
podman rm $POSTGRES_CONTAINER || true

# Start PostgreSQL container
podman run -d \
  --name $POSTGRES_CONTAINER \
  --network $NETWORK_NAME \
  -e POSTGRES_USER=${POSTGRES_USER} \
  -e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
  -e POSTGRES_DB=${POSTGRES_DB} \
  -p $POSTGRES_PORT:5432 \
  -v $POSTGRES_VOLUME:/var/lib/postgresql/data \
  $POSTGRES_IMAGE

echo "PostgreSQL container started. Use 'podman logs $POSTGRES_CONTAINER' to view logs." 