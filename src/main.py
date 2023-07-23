# main.py

from flask import Flask, request, jsonify

from src.web_scraper import WebScraper
from src.search import SearchEngine
from src import logger, config

app = Flask(__name__)


@app.route(config.SCRAPE_ROUTE, methods=["POST"])
def scrape_data():
    try:
        url = request.json["url"]
        scraper = WebScraper()
        data = scraper.scrape_and_save_data(url)
        return jsonify({"scraped_urls": list(data)})
    except KeyError:
        logger.error("Invalid input data. Make sure 'url' is provided in the JSON body.")
        return jsonify({"error": "Invalid input data. Make sure 'url' is provided in the JSON body."}), 400
    except Exception as e:
        logger.error("Exception while scraping data: ".format(e))
        return jsonify({"error": "An error occurred while scraping data."}), 500


@app.route(config.SEARCH_ROUTE, methods=["POST"])
def search_text():
    try:
        text = request.json["query"]
        search_engine = SearchEngine()
        result = search_engine.search_text(text)
        return jsonify({"result": result})
    except KeyError:
        logger.error("Invalid input data. Make sure 'query' is provided in the JSON body.")
        return jsonify({"error": "Invalid input data. Make sure 'text' is provided in the JSON body."}), 400
    except Exception as e:
        logger.error("Error while searching text: ".format(e))
        return jsonify({"error": "An error occurred while searching query."}), 500


if __name__ == "__main__":
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=True)
