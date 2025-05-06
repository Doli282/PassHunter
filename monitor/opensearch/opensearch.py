"""OpenSearch client connection"""
import os
from typing import Any

from opensearchpy import OpenSearch


# TODO chunking does not work
# Define the ingest pipeline
txt_pipeline_body = {
  "description": "Extract attachment information and chunk text",
  "processors": [
    {
      "attachment": {
        "field": "data",
        "target_field": "attachment"
      }
    },
    {
      "set": {
        "field": "document_content",
        "value": "{{attachment.content}}"
      }
    },
    {
      "text_chunking": {
        "algorithm": {
          "delimiter": {
            "delimiter": 'n',
            "max_chunk_limit": -1
          }
        },
        "field_map": {
          "document_content": "passage_chunk"
        }
      }
    },
    {
      "remove": {
        "field": "attachment"
      }
    },
    {
      "remove": {
        "field": "document_content"
      }
    }
  ]
}



class Client(OpenSearch):
    """Custom client for OpenSearch with added shortcut functions."""
    def __init__(self, init_pipeline: str = 'txt_pipeline', init_index: str = 'documents'):
        """
        Initialize the OpenSearch client.

        Args:
            init_pipeline (str): The name of the ingest pipeline to initialize.
            init_index (str): The name of the index to initialize.
        """
        super().__init__(
            hosts=[{'host': os.getenv("OPENSEARCH_HOST", 'localhost'), "port": os.getenv("OPENSEARCH_PORT", 9200)}],
            http_compress = True, # enables gzip compression for request bodies
            http_auth = (os.getenv("OPENSEARCH_USER"), os.getenv("OPENSEARCH_ADMIN_PASSWORD")),
            use_ssl = True,
            verify_certs = False,
            ssl_assert_hostname = False,
            ssl_show_warn = False,
        )
        # Create the ingest pipeline
        if init_pipeline:
            self.ingest.put_pipeline(id=init_pipeline, body=txt_pipeline_body)
        # Set the index
        self.set_index = init_index

    def search_term(self, search_term: str, search_index: str = None) -> Any:
        """
        Search the index for a given term.

        Args:
            search_term (str): The search term.
            search_index (str): The index to search.

        Returns:
            Response from OpenSearch.
        """
        # Define search body
        search_body = {
            "query": {
                "match": {
                    "passage_chunk.content": search_term
                }
            }
        }

        index = search_index if search_index else self.set_index
        self.indices.refresh(index=index)
        return self.search(index=index, body=search_body)
