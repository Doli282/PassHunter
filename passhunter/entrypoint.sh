#!/bin/bash

echo "----- Initializing -----"
flask db init
echo "----- Migrating -----"
flask db migrate
echo "----- Upgrading -----"
flask db upgrade
echo "----- Creating -----"
python manage.py create_db


# Start the Flask application
echo "Starting PassHunter application..."
python passhunter.py
