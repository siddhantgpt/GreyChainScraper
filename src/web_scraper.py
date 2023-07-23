# web_scraper.py

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.data_manager import DataManager
from src import logger, config


class WebScraper:
    def __init__(self):
        self.data_manager = DataManager()
        self.visited_urls = set()
        self.child_urls = set()
        self.scraped_data = {}
        self.session = requests.Session()

    def scrape_and_save_data(self, url):
        logger.info("Got request to scrape data for url and its child: {}".format(url))
        self.scrape_data(url, True)

        with ThreadPoolExecutor(max_workers=config.MAX_WORKER) as executor:
            futures = [executor.submit(self.scrape_data, url) for url in self.child_urls]
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logger.error("Error while scraping child url".format(e))

        self.data_manager.save_data(self.scraped_data)

        return list(self.visited_urls)

    def scrape_data(self, url, is_parent_url=False):
        if url in self.visited_urls:
            logger.info("Skipping url as it is already visited: {}".format(url))
            return

        try:
            response = self.session.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                self.scraped_data[url] = soup.get_text()
                self.visited_urls.add(url)
                logger.info("url scraped successfully: {}".format(url))
                if is_parent_url:
                    self.get_child_urls(soup, url)
                return
            else:
                logger.error("Failed to get response from url: {}, status code: {}".format(url, response.status_code))
        except Exception as e:
            logger.error("Exception while scraping url:{}".format(url, e))

    def get_child_urls(self, soup, parent_url):
        links = soup.find_all("a")
        self.child_urls = [link.get("href") for link in links if
                           link.get("href") and link.get("href") not in self.visited_urls
                           and link.get("href").startswith(parent_url)]
