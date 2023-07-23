# test_web_scraper.py

import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
from src.web_scraper import WebScraper


class WebScraperTest(unittest.TestCase):
    def setUp(self):
        self.scraper = WebScraper()

    @patch("src.web_scraper.WebScraper.scrape_data")
    @patch("src.web_scraper.DataManager.save_data")
    def test_scrape_and_save_data(self, mock_save_data, mock_scrape_data):
        url = "https://example.com"
        self.scraper.child_urls = [
            "https://example.com/child1",
            "https://example.com/child2",
            "https://example.com/child3",
        ]
        self.scraper.scrape_and_save_data(url)

        expected_calls = [
            mock.call(url, True),
            mock.call("https://example.com/child1"),
            mock.call("https://example.com/child2"),
            mock.call("https://example.com/child3"),
        ]
        mock_scrape_data.assert_has_calls(expected_calls)
        mock_save_data.assert_called_once()

    @patch("src.web_scraper.requests.Session.get")
    def test_scrape_data_success(self, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.content = b"<html><body>Hello, Grey Chain!</body></html>"
        url = "https://example.com"
        self.scraper.scrape_data(url)

        self.assertIn(url, self.scraper.visited_urls)
        self.assertIn(url, self.scraper.scraped_data)
        self.assertEqual(self.scraper.scraped_data[url], "Hello, Grey Chain!")

    @patch("src.web_scraper.requests.Session.get")
    @patch("src.logger.error")
    def test_scrape_data_fail(self, mock_error, mock_get):
        mock_response = mock_get.return_value
        mock_response.status_code = 404
        url = "https://example.com"
        self.scraper.scrape_data(url)

        self.assertNotIn(url, self.scraper.visited_urls)
        self.assertNotIn(url, self.scraper.scraped_data)
        self.assertTrue(mock_error.called)
        mock_error.assert_called_once_with("Failed to get response from url: {}, status code: 404".format(url))

    @patch("requests.Session.get", side_effect=Exception("Connection error"))
    @patch("src.logger.error")
    def test_scrape_data_exception(self, mock_error, mock_get):
        url = "https://example.com"
        self.scraper.scrape_data(url)
        self.assertNotIn(url, self.scraper.visited_urls)
        self.assertNotIn(url, self.scraper.scraped_data)
        self.assertTrue(mock_error.called)
        mock_error.assert_called_once_with("Exception while scraping url:{}".format(url))

    def test_get_child_urls(self):
        soup_mock = MagicMock()
        soup_mock.find_all.return_value = [
            MagicMock(get=lambda attr: "https://example.com/child1"),
            MagicMock(get=lambda attr: "https://example.com/child2"),
            MagicMock(get=lambda attr: "https://example.com/child3"),
        ]

        self.scraper.get_child_urls(soup_mock, "https://example.com")
        expected_child_urls = [
            "https://example.com/child1",
            "https://example.com/child2",
            "https://example.com/child3",
        ]
        self.assertEqual(self.scraper.child_urls, expected_child_urls)


if __name__ == "__main__":
    unittest.main()
