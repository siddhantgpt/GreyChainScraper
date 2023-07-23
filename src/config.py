# config.py

## Server
APP_HOST = "0.0.0.0"
APP_PORT = 8080

## Logging
LOGGER_NAME = "WEB_SCRAPER"
LOGGER_PATH = "../logs/"
LOGGER_FILE = "web_scraper.log"

## Data
DATA_PATH = "../scraped_data/"
DATA_FILE = "scraped_data.json"

# Routes
SCRAPE_ROUTE = "/scrape"
SEARCH_ROUTE = "/search"

## Concurrency
MAX_WORKER = 10
