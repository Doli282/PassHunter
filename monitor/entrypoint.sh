#!/bin/sh
# Change ownership of the mounted volume
chown -R hunter:huntergroup /data

# Execute the main application as the non-root user
gosu hunter celery -A monitor worker --loglevel="$LOGGING_LEVEL" --queues=uploads
