# Installation

```shell
pip install python-dotenv
pip install celery
pip install opensearch-py
```

# OpenSearch

Split processor:
https://docs.opensearch.org/docs/latest/ingest-pipelines/processors/split/

Boolean query:
https://docs.opensearch.org/docs/latest/query-dsl/compound/bool/


## Upload

### single upload vs bulk

According to the documentation, it is better, performance-wise, to upload data in a bulk.
https://docs.opensearch.org/docs/latest/api-reference/document-apis/bulk/

### Parsing

There are basically three main options:
1. upload the file as a whole
2. preprocess the file and divide it into chunks, before upload
3. parse the file and store specific fields with values

#### 1. Upload the whole file with ingest-attachment plugin.

It is possible to use the `ingest-attachment` plugin for OpenSearch in order to upload whole files.
The plugin is able to ingest files of different formats, like .docx, .pdf, .txt, ...
It accepts data encoded with base64.
The plugin tries to extract metadata from the file as well.

Searching then returns the whole file.

The ingest-attachment plugin needs to be installed, since it is not part of the basic installation of OpenSearch.
https://docs.opensearch.org/docs/latest/install-and-configure/additional-plugins/ingest-attachment-plugin/
```shell
./bin/opensearch-plugin install ingest-attachment
```

#### 2. Upload the whole file but split it into chunks

The ingest-attachment plugin can be used together with other processors to break the whole file into smaller parts.
Splitting into chunks can be done either in the script before calling the OpenSearch API or in the ingest pipeline.

A function in the python script could be used for reading the file line by line.
Then each line would be separately uploaded into OpenSearch.
This works well for files containing plain text, but it cannot be effectively used for other formats.

Splitting in the ingest pipeline can be done either with `text_chunking` processor or with the `split` processor.
The `text_chunking` processor is more powerful but cannot split data encoded with base64.
It still returns the whole file in one field in the json response.

```json
{
    "text_chunking": {
        "ignore_missing": true,
        "algorithm": {
            "delimiter": {
                "delimiter": "\n",
                "max_chunk_limit": -1
            }
        },
        "field_map": {
            "attachment.content": "attachment_parts"
        }
    }
}
```
https://docs.opensearch.org/docs/latest/ingest-pipelines/processors/text-chunking/

The `split` processor has fewer functions, but it can divide the file into a field array.
```json
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
                "field": "attachment"
            }
        },
        {
            "remove": {
                "field": "data"
            }
        }
    ]
}
```
https://docs.opensearch.org/docs/latest/ingest-pipelines/processors/split/

It returns the chunks in a list.
That means that when doing a simple query, all fields are returned.
However, when highlighting is used in the query, OpenSearch returns the fields with the searched term in a separate list.
```json
{
    "query": {
        "bool": {
            "must": {
                "match": {
                    "attachment_parts": search_term
                }
            }
        }
    },
    "highlight": {
        "fields": {
            "attachment_parts": {}
        }
    }
}
```
https://docs.opensearch.org/docs/latest/search-plugins/searching-data/highlight/

#### 3. Parsing

Parsing files is possible only when the files follow a predefined static structure.
Files processed by the application may follow some kind of structure, but it is not certain.
Some files have different structures from other files.


# Files

hashing: https://docs.python.org/3/library/hashlib.html#hashlib.file_digest
hash stored as LargeBinary -> transforms into bytea in PG https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.LargeBinary
