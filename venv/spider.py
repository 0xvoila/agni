import scrapy
from bs4 import BeautifulSoup, SoupStrainer


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'https://en.wikipedia.org/wiki/Main_Page',
    ]

    def parse(self, response):

        filename = "abc.html"
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')

        for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
            if link.has_attr('href'):
                next_page = response.urljoin(link['href'])
                yield scrapy.Request(next_page, callback=self.parse)