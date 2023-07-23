# search.py

from src.data_manager import DataManager
from src import logger


class SearchEngine:
    def __init__(self):
        self.data_manager = DataManager()

    def search_text(self, text):
        found_pages = []
        scraped_data = self.data_manager.load_data()
        for url, page_data in scraped_data.items():
            if text.lower() in page_data.lower():
                found_pages.append(url)
                logger.info("Text '{}' found in {}".format(text, url))
        logger.info("Text '{}' found in {} pages".format(text, len(found_pages)))
        return found_pages
