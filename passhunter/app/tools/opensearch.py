"""OpenSearch client connection"""
import os

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
        # Set the ingest pipeline
        self.pipeline_id = pipeline_id
        # Set the index
        self.index_id = index_id

    def search_term(self, search_term: str) -> tuple[int, dict[list[str]]]:
        """
        Search the index for a given term.

        Args:
            search_term (str): The search term.

        Returns:
            Tuple of hit count and list of lists for highlighted matches.
        """
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

        # Perform the actual search and return the response
        response = self.search(index=self.index_id, body=search_body)
        # Get the number of total hits
        count = response.get("hits", {}).get("total", {}).get("value", 0)
        # Get all highlights in a dictionary. The key is the filename where they were found.
        hits = response.get("hits", {}).get("hits", [])
        matches = {}
        for hit in hits:
            matches[hit.get("_source", {}).get("filename", "unknown")] = hit.get("highlight", {}).get(
                "attachment_parts", [])
        return count, matches
