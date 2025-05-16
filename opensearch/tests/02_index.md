# TC_02_Index

Test the definition of an index.

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

Defined index:
```shell
curl -XPUT -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/my_index" -H 'Content-Type: application/json' -d'
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "classic"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "filename": {
        "type": "keyword"
      },
      "uploaded_at": {
        "type": "date"
      },
      "attachment_parts":{
          "type": "text",
          "analyzer": "my_analyzer",
          "search_analyzer": "my_analyzer"
      }
    }
  }
}
'
```

## Steps

Check the existence of the index:
```shell
curl -XGET -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/_list/indices"
```

Run a simulation of generated tokens:
```shell
curl -XPOST -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/my_index/_analyze" -H 'Content-Type: application/json' -d'
{
  "analyzer": "my_analyzer",
  "text": "Url:http://www.security.com/login/new\nUsername:goerge@gmail.com\nPassword:Password.my.strong\n==============\npass: account@email.com\nurl:https://name:password@example.com/index#fragment?query=sdf"
}
'
```

## Expected Result

The result of the simulation is the following:
```json
{
  "tokens": [
    {
      "token": "Url",
      "start_offset": 0,
      "end_offset": 3,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "http",
      "start_offset": 4,
      "end_offset": 8,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "www.security.com",
      "start_offset": 11,
      "end_offset": 27,
      "type": "<HOST>",
      "position": 2
    },
    {
      "token": "login",
      "start_offset": 28,
      "end_offset": 33,
      "type": "<ALPHANUM>",
      "position": 3
    },
    {
      "token": "new",
      "start_offset": 34,
      "end_offset": 37,
      "type": "<ALPHANUM>",
      "position": 4
    },
    {
      "token": "Username",
      "start_offset": 38,
      "end_offset": 46,
      "type": "<ALPHANUM>",
      "position": 5
    },
    {
      "token": "goerge@gmail.com",
      "start_offset": 47,
      "end_offset": 63,
      "type": "<EMAIL>",
      "position": 6
    },
    {
      "token": "Password",
      "start_offset": 64,
      "end_offset": 72,
      "type": "<ALPHANUM>",
      "position": 7
    },
    {
      "token": "Password.my.strong",
      "start_offset": 73,
      "end_offset": 91,
      "type": "<HOST>",
      "position": 8
    },
    {
      "token": "pass",
      "start_offset": 107,
      "end_offset": 111,
      "type": "<ALPHANUM>",
      "position": 9
    },
    {
      "token": "account@email.com",
      "start_offset": 113,
      "end_offset": 130,
      "type": "<EMAIL>",
      "position": 10
    },
    {
      "token": "url",
      "start_offset": 131,
      "end_offset": 134,
      "type": "<ALPHANUM>",
      "position": 11
    },
    {
      "token": "https",
      "start_offset": 135,
      "end_offset": 140,
      "type": "<ALPHANUM>",
      "position": 12
    },
    {
      "token": "name",
      "start_offset": 143,
      "end_offset": 147,
      "type": "<ALPHANUM>",
      "position": 13
    },
    {
      "token": "password@example.com",
      "start_offset": 148,
      "end_offset": 168,
      "type": "<EMAIL>",
      "position": 14
    },
    {
      "token": "index",
      "start_offset": 169,
      "end_offset": 174,
      "type": "<ALPHANUM>",
      "position": 15
    },
    {
      "token": "fragment",
      "start_offset": 175,
      "end_offset": 183,
      "type": "<ALPHANUM>",
      "position": 16
    },
    {
      "token": "query",
      "start_offset": 184,
      "end_offset": 189,
      "type": "<ALPHANUM>",
      "position": 17
    },
    {
      "token": "sdf",
      "start_offset": 190,
      "end_offset": 193,
      "type": "<ALPHANUM>",
      "position": 18
    }
  ]
}
```

## Cleanup

Delete an unused index:
```shell
curl -XDELETE -k -u "${OPENSEARCH_USER}:${OPENSEARCH_ADMIN_PASSWORD}" "https://${OPENSEARCH_HOST}:${OPENSEARCH_PORT}/my_index"
```