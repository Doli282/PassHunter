# TC_01_Pipeline

Test the definition of a pipeline.

## Preconditions

- running opensearch
- defined environment variables:
```dotenv
# OpenSearch Configuration
OPENSEARCH_HOST=localhost
OPENSEARCH_PORT=9200
OPENSEARCH_USER=
OPENSEARCH_ADMIN_PASSWORD=
```

Defined pipeline:
```shell
curl -XPUT -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/_ingest/pipeline/my_pipeline" -H 'Content-Type: application/json' -d'
{
    "description": "Extract attachment information and chunk text",
    "processors": [
        {
            "attachment": {
                "field": "data",
                "target_field": "attachment"
            }
        },
        {
            "split": {
                "field": "attachment.content",
                "separator": "\n",
                "target_field": "attachment_parts"
            }
        },
        {
            "remove": {
                "field": "attachment.content"
            }
        },
        {
            "remove": {
                "field": "data"
            }
        }
    ]
}
'
```

## Steps

Run a simulation of the pipeline

```shell
read -r -d '' JSON_BODY <<EOF
{
  "docs": [
    {
      "_index": "my-index",
      "_id": "test-doc-1",
      "_source": {
        "data": "$(base64 -w 0 "test_data/test_input.txt")",
        "filename": "test_filename",
        "uploaded_at": "2025-05-16T23:59:00"
      }
    }
  ]
}
EOF

curl -XPOST -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/_ingest/pipeline/my_pipeline/_simulate" -H 'Content-Type: application/json' -d "$JSON_BODY"
```

## Expected Result

The expected output from the pipeline looks like this. E.g., the `_ingest.timestamp` will be different.
```json
{
  "docs": [
    {
      "doc": {
        "_index": "my-index",
        "_id": "test-doc-1",
        "_source": {
          "filename": "test_filename",
          "attachment_parts": [
            "Url:https://portal.gouda.com/login\r",
            "Username:john@gmail.com\r",
            "Password:john54321\r",
            "===============================================================\r",
            "Url:http://www.security.com/login/new\r",
            "Username:george@gmail.com\r",
            "Password:george@54321\r",
            "==============================================================="
          ],
          "attachment": {
            "content_type": "text/plain; charset=windows-1252",
            "language": "en",
            "content_length": 299
          },
          "uploaded_at": "2025-05-16T23:59:00"
        },
        "_ingest": {
          "timestamp": "2025-05-13T10:04:53.11297995Z"
        }
      }
    }
  ]
}
```

## Cleanup

Remove the pipeline if it is no longer used.
```shell
curl -XDELETE -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/_ingest/pipeline/my_pipeline"
```
