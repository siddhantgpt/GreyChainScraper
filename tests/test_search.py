# test_search.py

import unittest
from unittest.mock import patch

from src.search import SearchEngine


class SearchEngineTestCase(unittest.TestCase):

    def setUp(self):
        self.search_engine = SearchEngine()

    @patch("src.data_manager.DataManager.load_data")
    def test_search_text_found(self, mock_data):
        data = {
            "https://example.com/page1": "This is a test page containing the word text.",
            "https://example.com/page2": "Another test page with the word text.",
            "https://example.com/page3": "No match here.",
        }
        mock_data.return_value = data
        text = "text"
        result = self.search_engine.search_text(text)

        expected_result = ["https://example.com/page1", "https://example.com/page2"]
        self.assertEqual(result, expected_result)
        mock_data.assert_called_once_with()

    @patch("src.data_manager.DataManager.load_data")
    def test_search_text_not_found(self, mock_data):
        data = {
            "https://example.com/page1": "This is a test page.",
            "https://example.com/page2": "Another test page.",
        }
        mock_data.return_value = data
        text = "text"
        result = self.search_engine.search_text(text)

        expected_result = []
        self.assertEqual(result, expected_result)
        mock_data.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
