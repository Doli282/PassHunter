#!/bin/bash

# Start the Flask application
echo "Initializing database"
/usr/src/passhunter/db_init.sh
echo "Starting PassHunter application..."
python passhunter.py
