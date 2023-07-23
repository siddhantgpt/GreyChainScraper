# GreyChainScraper
A web scraper created in python that can scrape data from a URL and its child URLs and can search keyword from the scraped data.

**Steps to setup on windows:**
1. cd <"directory where reposirory is cloned">
2. git clone https://github.com/siddhantgpt/GreyChainScraper.git
3. cd GreyChainScraper
4. run_web_scrapper.bat

The project should now be running on your machine.



**Scrape data**

Go to Postman and import the following curl:

curl --location 'http://localhost:8080/scrape' \
--header 'Content-Type: application/json' \
--data '{
    "url": <"Your URL, example: https://greychaindesign.com/">
}'



**Search Keyword**

Go to Postman and import the following curl:

curl --location 'http://localhost:8080/search' \
--header 'Content-Type: application/json' \
--data '{
    "query": <"Your Keyword, example: Grey Chain">
}'


**Some features of the project**

1. Scraping is done for the URL as well as for all the child URLs.
2. Searching for keywords returns the URLs where the keywords is present.
3. Search is case insensitive.
4. Project is automated to be intalled, built, tested and run on windows.
5. Concurrency is used for performance enhancement while scraping data.
6. Logging is provided on all levels.
7. Test cases have been written for all the methods in the code.

