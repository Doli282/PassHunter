"""OpenSearch client connection"""
import os
from typing import Any

from opensearchpy import OpenSearch


class Client(OpenSearch):
    """Custom client for OpenSearch with added shortcut functions."""
    def __init__(self, pipeline_id: str = 'attachment_pipeline', index_id: str = 'infostealers_classic'):
        """
        Initialize the OpenSearch client.

        Args:
            pipeline_id (str): The name of the ingest pipeline to initialize.
            index_id (str): The name of the index to initialize.
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
        self.pipeline_id = pipeline_id
        self._create_index_pipeline()
        # Set and create the index
        self.index_id = index_id
        if not self.indices.exists(index=self.index_id):
            self._create_index()

    def upload_file(self, encoded_data: str, filename: str, uploaded_at: str) -> Any:
        """
        Upload a file to OpenSearch.

        Args:
            encoded_data (str): The encoded data.
            filename (str): The filename.
            uploaded_at (str): The uploaded at date.

        Returns:
            Response from OpenSearch.
        """
        # Prepare the document to be uploaded
        document = self._prepare_document(encoded_data, filename, uploaded_at)
        return self.index(index=self.index_id, pipeline=self.pipeline_id, body=document)

    def prepare_bulk_upload(self, encoded_data: str, filename: str, uploaded_at: str) -> dict:
        """
        Prepare a bulk indexing action.

        Args:
            encoded_data (str): The encoded data.
            filename (str): The filename.
            uploaded_at (str): The uploaded at date.

        Returns:
            dict: The prepared bulk action.
        """
        return {
            '_op_type': 'index',
            '_index': self.index_id,
            'pipeline': self.pipeline_id,
            '_source': self._prepare_document(encoded_data, filename, uploaded_at)
        }

    def search_term(self, search_term: str, uploaded_at: str = None, search_index: str = None) -> Any:
        """
        Search the index for a given term.

        Args:
            search_term (str): The search term.
            uploaded_at (str): The uploaded at date.
            search_index (str): The index to search.

        Returns:
            Response from OpenSearch.
        """
        search_body = self._prepare_search_body(search_term, uploaded_at)

        # Use the default index if not directly specified
        index = search_index if search_index else self.index_id
        # Refresh the indexes before search
        self.indices.refresh(index=index)
        # Perform the actual search and return the response
        return self.search(index=index, body=search_body)

    def _create_index(self) -> Any:
        """
        Create an index.
        Define Tokenizer and Analyzer for the index.

        Returns:
            Response from OpenSearch.
        """
        index_body = {
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
                        "attachment_parts": {
                            "type": "text",
                            "analyzer": "my_analyzer",
                            "search_analyzer": "my_analyzer"
                        }
                    }
                }
            }
        return self.indices.create(index=self.index_id, body=index_body)

    def _create_index_pipeline(self) -> Any:
        """
        Create an index pipeline.
        The pipeline is used for extracting attachment information and chunking text.
        Removes fields with the original data after processing.

        Returns:
            Response from OpenSearch.
        """
        # Define the ingest pipeline
        pipeline_body = {
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
        return self.ingest.put_pipeline(id=self.pipeline_id, body=pipeline_body)

    def _prepare_document(self, encoded_data: str, filename: str, uploaded_at: str) -> dict:
        """
        Prepare the document to be uploaded.
        The document is used for uploading to OpenSearch.

        Args:
            encoded_data (str): The encoded data.
            filename (str): The filename.
            uploaded_at (str): The uploaded at date.

        Returns:
            dict: The prepared document.
        """
        # Prepare the document to be uploaded
        document = {
            "data": encoded_data,
            "filename": filename,
            "uploaded_at": uploaded_at
        }

        return document

    def _prepare_search_body(self, search_term: str, uploaded_at: str = None) -> dict:
        """
        Prepare the search body for search using wildcard.

        Args:
            search_term (str): The search term.
            uploaded_at (str): The uploaded at date.
            filename (str): The filename identifier.

        Returns:
            dict: The prepared search body.
        """
        # Define search body
        search_body = {
            "query": {
                "bool": {
                    "must": {
                        "wildcard": {
                            "attachment_parts": search_term
                        }
                    }
                }
            },
            "highlight": {
                "pre_tags": [
                    ""
                ],
                "post_tags": [
                    ""
                ],
                "fields": {
                    "attachment_parts": {}
                }
            }
        }

        if uploaded_at:
            search_body["query"]["bool"]["filter"] = {"term": {"uploaded_at": uploaded_at}}

        return search_body
