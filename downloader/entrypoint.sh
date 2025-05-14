#!/bin/sh
# Change ownership of the mounted volume
chown -R hunter:huntergroup /data

# Execute the main application as the non-root user
gosu hunter python -u downloader.py
