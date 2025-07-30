
Goojara Scraper
This is a Scrapy spider designed to scrape movie and series data from Goojara (ww1.goojara.to). It extracts information such as title, thumbnail, movie genre, release date, description, directors, and cast.

Project Structure
The provided image shows the project structure:

.
├── upwork-scrapin...
│   └── Moviescrapr
│       ├── .scrapy
│       └── Moviescrapr
│           ├── __pycache__
│           ├── spiders
│           │   ├── __pycache__
│           │   ├── __init__.py
│           │   └── goojara.py  <-- The spider
│           ├── __init__.py
│           ├── items.py
│           ├── mid (C:\Users\HP\Des\folder\Moviescrapr)
│           ├── pipe
│           └── settings.py
├── requirements.txt
└── scrapy.cfg
The core logic for scraping Goojara resides in goojara.py within the Moviescrapr/Moviescrapr/spiders/ directory.

Features
Pagination Handling: Scrapes movie links across the first 200 pages of Goojara's movie listings.

Detail Extraction: Navigates to individual movie/series pages to extract detailed information.

Data Fields: Extracts the following data points for each movie/series:

film_link: The URL of the movie/series page.

title: The title of the movie/series.

thumbnail: The URL of the movie/series thumbnail image.

movie_generic: The genre of the movie/series.

release_date: The release date of the movie/series.

description: A brief description of the movie/series.

directors: The directors of the movie/series.

cast: The main cast of the movie/series.

Installation
Clone the repository:

Bash

git clone https://github.com/your-username/your-repository-name.git
cd your-repository-name
Install Scrapy and other dependencies:
It's recommended to use a virtual environment.

Bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
pip install -r requirements.txt
(Ensure you have a requirements.txt file in your project root with Scrapy listed, or just pip install Scrapy directly if not.)

Usage
To run the spider, navigate to the root directory of your Scrapy project (the directory containing scrapy.cfg) and execute the following command:

Bash

scrapy crawl goojara -o goojara_data.json
This command will:

Start the goojara spider.

Save the scraped data to a JSON file named goojara_data.json.

You can change the output format (e.g., CSV, XML) by changing the file extension in the -o flag. For example, to output to CSV:

Bash

scrapy crawl goojara -o goojara_data.csv
Code Explanation
goojara.py
Python

import scrapy

class GoojaraSpider(scrapy.Spider):
    name = "goojara"
    allowed_domains = ["ww1.goojara.to"]
    start_urls = (
        [f"https://ww1.goojara.to/watch-movies?p={i}" for i in range(1, 200)]
    )

    def parse(self, response):
        # This is the list page: get links to individual movies/series
        for link in response.css('div.mxwd div.dflex a::attr(href)').getall():
            full_link = response.urljoin(link)
            yield scrapy.Request(url=full_link, callback=self.parse_detail)

    def parse_detail(self, response):
        container = response.css('div.marl div.date::text').getall()
        description_container = response.css('div.marl div.fimm p::text').getall()

        yield {
            'film_link': response.url,
            'title': response.css('div.marl h1::text').get(),
            'thumbnail': response.css('div.imrl img::attr(src)').get(),
            'movie_generic': container[1] if len(container) > 1 else '',
            'release_date': container[2] if len(container) > 2 else '',
            'description': description_container[0] if len(description_container) > 0 else '',
            'directors': description_container[1] if len(description_container) > 1 else '',
            'cast': description_container[2] if len(description_container) > 2 else '',
        }

name = "goojara": Defines the unique name of the spider.

allowed_domains = ["ww1.goojara.to"]: Specifies the domains that the spider is allowed to crawl. Requests to other domains will be ignored.

start_urls: A list of URLs where the spider will begin crawling. In this case, it generates URLs for the first 200 movie listing pages.

parse(self, response): This method is called for each URL in start_urls. It's responsible for parsing the initial response and extracting links to individual movie/series detail pages.

It selects all <a> tags within div.mxwd div.dflex to get the movie links.

response.urljoin(link) constructs absolute URLs from relative ones.

yield scrapy.Request(url=full_link, callback=self.parse_detail) creates a new request for each detail page and specifies parse_detail as the callback function to handle its response.

parse_detail(self, response): This method is called for each individual movie/series detail page. It extracts the desired information using CSS selectors.

response.css(...) is used to select elements based on their CSS selectors.

.get() retrieves the first matching element's text or attribute.

.getall() retrieves all matching elements' texts or attributes.

The extracted data is yielded as a dictionary, which Scrapy will then process (e.g., save to a file, pass to pipelines). The conditional checks (if len(container) > 1 else '') are used to prevent IndexError if a particular data point is missing on a page.

Contributing
Feel free to open issues or submit pull requests to improve this scraper.

