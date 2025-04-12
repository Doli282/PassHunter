#!/bin/bash
for file in ./data/*.txt; do
  encoded=$(base64 -w 0 "$file")
  curl -k -X POST "https://localhost:9200/alala/_doc/?pipeline=attachment" \
    -u "admin:0896Nokie*" \
    -H 'Content-Type: application/json' \
    -d "{\"data\": \"$encoded\"}"
done
