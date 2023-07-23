# test_main.py

import unittest
from unittest.mock import patch

from src.main import app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @patch("src.web_scraper.WebScraper.scrape_and_save_data", return_value=["https://example.com"])
    def test_scrape_data_success(self, mock_scraper):
        response = self.app.post("/scrape", json={"url": "https://example.com"})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["scraped_urls"], ["https://example.com"])
        mock_scraper.assert_called_once_with("https://example.com")

    def test_scrape_data_missing_url(self):
        response = self.app.post("/scrape", json={})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual("Invalid input data. Make sure 'url' is provided in the JSON body.", data['error'])

    @patch("src.web_scraper.WebScraper.scrape_and_save_data", side_effect=Exception("Error"))
    def test_scrape_data_exception(self, mock_scraper):
        response = self.app.post("/scrape", json={"url": "example.com"})
        data = response.get_json()

        self.assertEqual(response.status_code, 500)
        self.assertIn('error', data)
        self.assertEqual("An error occurred while scraping data.", data['error'])

    @patch("src.search.SearchEngine.search_text", return_value=["https://example.com"])
    def test_search_text_success(self, mock_search_engine):
        response = self.app.post("/search", json={"query": "example"})
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["result"], ["https://example.com"])
        mock_search_engine.assert_called_once_with("example")

    def test_search_text_missing_query(self):
        response = self.app.post("/search", json={})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual("Invalid input data. Make sure 'text' is provided in the JSON body.", data['error'])

    @patch("src.search.SearchEngine.search_text", side_effect=Exception("Error"))
    def test_search_text_exception(self, mock_search_engine):
        response = self.app.post("/search", json={"query": "example"})
        data = response.get_json()

        self.assertEqual(response.status_code, 500)
        self.assertIn('error', data)
        self.assertEqual("An error occurred while searching query.", data['error'])


if __name__ == "__main__":
    unittest.main()
