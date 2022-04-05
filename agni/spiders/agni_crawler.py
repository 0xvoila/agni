import scrapy
from bs4 import BeautifulSoup, SoupStrainer
import urllib
import json
from urllib.parse import urlparse
from py2neo import Graph
import boto3

class AgniSpider(scrapy.Spider):
    name = "agni"
    graph = Graph(password="2June1989!", name="neo4j")
    start_urls = [
        'https://en.wikipedia.org/wiki/Main_Page',
    ]

    client = boto3.client('firehose')

    def parse(self, response):

        url = response.request.url
        soup = BeautifulSoup(response.text, 'lxml')

        d = {}
        for element in soup.find_all():
            if element.name == "html" or element.name == "body":
                pass

            else:
                x = element.find_all(text=True, recursive=False)
                if x:
                    d[element.name] = x

        client.put_record(
            DeliveryStreamName='PUT-OPS-ltrsw',
            Record={
                'Data': json.dumps(d)
            }
        )

        for link in soup.find_all('a', href=True):
            absoluteUrl = urllib.parse.urljoin(url, link['href'])
            parsedUrl = urlparse(absoluteUrl)
            if parsedUrl.scheme.strip().lower() != 'https' and parsedUrl.scheme.strip().lower() != 'http':
                pass
            else:

                self.graph.run(
                    "MERGE (child:page{page_url:'" + url + "'}) " +
                    "On CREATE " +
                    "SET child.page_url='" + url + "', page_rank = 1.0 " +
                    "MERGE (parent:page{page_url:'" + absoluteUrl + "'}) " +
                    "On CREATE " +
                    "SET parent.page_url = '" + absoluteUrl + "' , page_rank = 1.0 " +
                    "MERGE (child)-[:FOLLOWS]->(parent)"
                )

                yield response.follow(absoluteUrl, callback=self.parse)

