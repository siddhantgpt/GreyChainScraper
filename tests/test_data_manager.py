# test_data_manager.py

import unittest
import os
import json
from unittest.mock import patch, mock_open

from src.data_manager import DataManager


class DataManagerTest(unittest.TestCase):
    def setUp(self):
        self.data_file = "test_data.json"
        self.data_manager = DataManager(self.data_file)

    def tearDown(self):
        if os.path.exists(self.data_file):
            os.remove(self.data_file)

    @patch("src.logger.info")
    @patch("src.logger.warning")
    def test_load_data_file_not_found(self, mock_warning, mock_info):
        data = self.data_manager.load_data()
        self.assertEqual(data, {})
        mock_info.assert_called_once_with("Loading scraped data from file {}".format(self.data_file))
        mock_warning.assert_called_once_with("Data file {} not found".format(self.data_file))

    @patch("src.logger.info")
    def test_load_data_file_found(self, mock_info):
        test_data = {"key1": "value1", "key2": "value2"}
        with open(self.data_file, "w") as file:
            json.dump(test_data, file)

        data = self.data_manager.load_data()
        self.assertEqual(data, test_data)
        mock_info.assert_called_once_with("Loading scraped data from file {}".format(self.data_file))

    @patch("src.logger.info")
    def test_save_data_success(self, mock_info):
        test_data = {"key1": "value1", "key2": "value2"}
        self.data_manager.save_data(test_data)

        with open("test_data.json", "r") as file:
            saved_data = json.load(file)
        self.assertEqual(test_data, saved_data)
        mock_info.assert_called_once_with("Data saved to file: {}".format(self.data_file))

    @patch("src.logger.error")
    @patch("builtins.open", side_effect=Exception("Error"))
    def test_save_data_failure(self, mock_file, mock_error):
        test_data = {"key1": "value1", "key2": "value2"}

        self.data_manager.save_data(test_data)
        mock_error.assert_called_once_with("Failed to save data to file: {}".format(self.data_file))


if __name__ == "__main__":
    unittest.main()
