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
