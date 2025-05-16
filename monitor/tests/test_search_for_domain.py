# Generated with PyCharm IDE with the feature "Generate Unit Tests" for search_for_domain() function

import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from monitor import search_for_domain

@patch("monitor.opensearch")
class TestSearchForDomain(unittest.TestCase):
    def setUp(self):
        self.mock_domain = MagicMock()
        self.mock_domain.name = "example.com"
        self.uploaded_at = datetime.now()

    def test_search_for_domain_success(self, mock_opensearch):
        """
        Test case for a successful search for a domain, ensuring proper hit count
        and match data extraction from the response.
        """
        mock_response = {
            "hits": {
                "total": {"value": 2},
                "hits": [
                    {"_source": {"filename": "file1.txt"}, "highlight": {"attachment_parts": ["match1", "match2"]}},
                    {"_source": {"filename": "file2.txt"}, "highlight": {"attachment_parts": ["match3"]}}
                ]
            }
        }
        mock_opensearch.search_term.return_value = mock_response

        result = search_for_domain(self.mock_domain, self.uploaded_at)

        self.assertEqual(result[0], 2)
        self.assertIn("file1.txt", result[1])
        self.assertIn("file2.txt", result[1])
        self.assertListEqual(result[1]["file1.txt"], ["match1", "match2"])
        self.assertListEqual(result[1]["file2.txt"], ["match3"])

    def test_search_for_domain_no_hits(self, mock_opensearch):
        """
        Test case where no results are found for a domain search.
        Ensures the hit count is 0 and matches are empty.
        """
        mock_response = {"hits": {"total": {"value": 0}, "hits": []}}
        mock_opensearch.search_term.return_value = mock_response

        result = search_for_domain(self.mock_domain, self.uploaded_at)

        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], {})

    def test_search_for_domain_invalid_uploaded_at(self, mock_opensearch):
        """
        Test case to verify search behavior with invalid 'uploaded_at' date formats.
        Ensures the method handles invalid cases correctly.
        """
        mock_response = {"hits": {"total": {"value": 1}, "hits": []}}
        mock_opensearch.search_term.return_value = mock_response

        result = search_for_domain(self.mock_domain, "invalid_date")

        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], {})

    def test_search_for_domain_missing_highlight(self, mock_opensearch):
        """
        Test case where search results do not include a highlight field.
        Ensures the method handles partial responses gracefully.
        """
        mock_response = {
            "hits": {
                "total": {"value": 1},
                "hits": [
                    {"_source": {"filename": "file1.txt"}, "highlight": {}}
                ]
            }
        }
        mock_opensearch.search_term.return_value = mock_response

        result = search_for_domain(self.mock_domain, self.uploaded_at)

        self.assertEqual(result[0], 1)
        self.assertIn("file1.txt", result[1])
        self.assertListEqual(result[1]["file1.txt"], [])


if __name__ == "__main__":
    unittest.main()
