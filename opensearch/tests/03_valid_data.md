# TC_03_Valid_data

Test upload, ingestion and search of a test dataset.

## Preconditions

- test 01_Pipeline
- test 02_Index

- defined pipeline
- defined index
- running opensearch
- defined environment variables:
```dotenv
# OpenSearch Configuration
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200
OPENSEARCH_USER=
OPENSEARCH_ADMIN_PASSWORD=
```

## Steps

Upload a test document to the defined index.
```shell
read -r -d '' JSON_BODY <<EOF
{
    "data": "$(base64 -w 0 "test_data/test_input.txt")",
    "filename": "test_filename",
    "uploaded_at": "2025-05-16T23:59:00"
}
EOF

curl -XPOST -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/my_index/_doc/987654321?pipeline=my_pipeline" -H 'Content-Type: application/json' -d"$JSON_BODY"
```

Check the file is there:
```shell
curl -XGET -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/my_index/_doc/987654321"
```

Run a search query for the desired string: 
```shell
curl -XGET -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/${index}/_search" -H 'Content-Type: application/json' -d'
{
    "query": {
        "bool": {
            "must": {
                "wildcard": {
                    "attachment_parts": "*gmail.com"
                }
            }
        }
    },
    "highlight": {
        "fields": {
            "attachment_parts": {}
        }
    }
}'
```



## Expected Result

The result highlights fields with the expanded searched string.
```shell
{
  "took": 6,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "my_index",
        "_id": "987654321",
        "_score": 1.0,
        "_source": {
          "filename": "test_filename",
          "attachment": {
            "content_type": "text/plain; charset=windows-1252",
            "language": "en",
            "content_length": 305
          },
          "uploaded_at": "2025-05-16T23:59:00",
          "attachment_parts": [
            "Url:https://portal.gouda.com/login\r",
            "Username:john@gmail.com\r",
            "Password:john54321\r",
            "===============================================================\r",
            "Url:http://www.security.com/login/new\r",
            "Username:goerge@gmail.com\r",
            "Password:Password.my.strong\r",
            "==============================================================="
          ]
        },
        "highlight": {
          "attachment_parts": [
            "Username:<em>john@gmail.com</em>",
            "Username:<em>goerge@gmail.com</em>"
          ]
        }
      }
    ]
  }
}
```

## Cleanup

Remove the test document.
```shell
curl -XDELETE -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/${index}/my_index/_doc/987654321"
```

