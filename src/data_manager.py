# data_manager.py

import json

from src import logger, config


class DataManager:
    def __init__(self, data_file=config.DATA_PATH + config.DATA_FILE):
        self.data_file = data_file

    def load_data(self):
        try:
            logger.info("Loading scraped data from file {}".format(self.data_file))
            with open(self.data_file, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            logger.warning("Data file {} not found".format(self.data_file))
            return {}

    def save_data(self, scraped_data):
        try:
            with open(self.data_file, "w") as file:
                json.dump(scraped_data, file)
            logger.info("Data saved to file: {}".format(self.data_file))
        except Exception as e:
            logger.error("Failed to save data to file: {}".format(self.data_file, e))
