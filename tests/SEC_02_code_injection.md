# SEC_02_Code_injection

Showing matched lines to the user may lead to stored Cross-site scripting attack.
Test what happens when data with malicious code is loaded to the database.
Test how the data is presented to the user.

## Preconditions

1. Prepare data with malicious code. E.g.:
```text
&lt;/TITLE&gt;&lt;SCRIPT&gt;alert(\"XSS\");&lt;/SCRIPT&gt;

SOFT: Chrome Default (131.0.6778.109)
URL: https://login.live.com/login.srf
USER: dummyuser
PASS: dummypassword

<img src=1 href=1 onerror="javascript:alert(1)"></img>
```

2. Have prepared Opensearch index and ingestion pipeline.
3. Run Opensearch instance and web GUI.
3. Set environment variables and test connection to OpenSearch instance.

## Steps

0. Check there is not a document with ID used in the next step. If there is one, find an unsued ID.
```shell
curl -XGET -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/infostealers_classic/_doc/987654321"
```
Expected answer:
```json
{"_index":"infostealers_classic","_id":"987654321","found":false}
```

1. Load the malicious code into OpenSearch.
```shell
read -r -d '' JSON_BODY <<EOF
{
    "data": "$(base64 -w 0 "tests/test_data/test_xss.txt")",
    "filename": "test_xss",
    "uploaded_at": "2025-05-16T23:59:00"
}
EOF

curl -XPOST -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/infostealers_classic/_doc/987654321?pipeline=attachment_pipeline" -H 'Content-Type: application/json' -d"$JSON_BODY"
```

2. Check the document has been uploaded.
```shell
curl -XGET -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/infostealers_classic/_doc/987654321"
```

3. In the web GUI search for a specific string from the test document ('onerror').

   
## Expected Result

The data is escaped and rendered as is.
The malicious code is not executed.
Expected result:
```text
Found 1 matches!
test_xss
<img src=1 href=1 onerror="javascript:alert(1)"></img> ANCHOR_STRING_2
```

## Cleanup

Remove the test document from the index:
```shell
curl -XDELETE -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/${index}/infostealers_classic/_doc/987654321"
```