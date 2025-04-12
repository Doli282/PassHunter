#!/bin/bash

# Source the configuration
source "$(dirname "$0")/config.sh"

# Create network if it doesn't exist
podman network create $NETWORK_NAME 2>/dev/null || true

# Build the web application image
podman build -t $WEB_APP_IMAGE ./gui

# Stop and remove existing container if it exists
podman stop $WEB_APP_CONTAINER || true
podman rm $WEB_APP_CONTAINER || true

# Start GUI container
podman run -d \
  --name $WEB_APP_CONTAINER \
  --network $NETWORK_NAME \
  -p $WEB_APP_PORT:5000 \
  -e "FLASK_APP=${FLASK_APP}" \
  -e "FLASK_ENV=${FLASK_ENV}" \
  -e "SECRET_KEY=${SECRET_KEY}" \
  -e "POSTGRES_HOST=$POSTGRES_CONTAINER" \
  -e "POSTGRES_PORT=$POSTGRES_PORT" \
  -e "POSTGRES_USER=$POSTGRES_USER" \
  -e "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" \
  -e "POSTGRES_DB=$POSTGRES_DB" \
  -e "OPENSEARCH_HOST=$OPENSEARCH_CONTAINER" \
  -e "OPENSEARCH_PORT=$OPENSEARCH_PORT" \
  -e "OPENSEARCH_USER=$OPENSEARCH_USER" \
  -e "OPENSEARCH_PASSWORD=$OPENSEARCH_PASSWORD" \
  -v $WEB_APP_VOLUME:/app \
  $WEB_APP_IMAGE

echo "GUI container started. Use 'podman logs $WEB_APP_CONTAINER' to view logs." 