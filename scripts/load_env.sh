#!/bin/bash

# Check if .env file exists
if [ ! -f "$(dirname "$0")/../.env" ]; then
    echo "Error: .env file not found!"
    exit 1
fi

# Read and export variables from .env file
while IFS='=' read -r key value || [ -n "$key" ]; do
    # Skip comments and empty lines
    [[ $key =~ ^#.*$ ]] && continue
    [[ -z $key ]] && continue
    
    # Remove any quotes and whitespace
    key=$(echo "$key" | tr -d ' ' | tr -d '"' | tr -d "'")
    value=$(echo "$value" | tr -d ' ' | tr -d '"' | tr -d "'")
    
    # Export the variable
    export "$key=$value"
done < "$(dirname "$0")/../.env"

echo "Environment variables loaded from .env file" 