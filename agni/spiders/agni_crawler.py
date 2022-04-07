import scrapy
from bs4 import BeautifulSoup, SoupStrainer
import urllib
import json
from urllib.parse import urlparse
from py2neo import Graph


# import base64


class AgniSpider(scrapy.Spider):
    name = "agni"
    # graph = Graph("bolt://44.202.30.181:7687", password="2June1989!", name="neo4j")
    graph = Graph(password="2June1989!", name="neo4j")
    start_urls = [
        'https://unbxd.com/docs/site-search/integration-documentation/',
    ]
    allowed_domains = ["unbxd.com"]

    def parse(self, response):

        url = response.request.url
        soup = BeautifulSoup(response.text, 'lxml')
        for link in soup.find_all('a', href=True):
            absoluteUrl = urllib.parse.urljoin(url, link['href'])
            parsedUrl = urlparse(absoluteUrl)
            if parsedUrl.scheme.strip().lower() != 'https' and parsedUrl.scheme.strip().lower() != 'http':
                pass
            else:

                url = url.replace("'", r"\'")
                absoluteUrl = absoluteUrl.replace("'", r"\'")
                # self.graph.run(
                #     "MERGE (child:page{page_url:'" + url + "'}) " +
                #     "On CREATE " +
                #     "SET child.page_url='" + url + "', child.page_rank = 1.0 " +
                #     "MERGE (parent:page{page_url:'" + absoluteUrl + "'}) " +
                #     "On CREATE " +
                #     "SET parent.page_url = '" + absoluteUrl + "' , parent.page_rank = 1.0 " +
                #     "MERGE (child)-[:FOLLOWS]->(parent)"
                # )

                yield scrapy.Request(absoluteUrl, callback=self.parseContent)

    def parseContent(self, response):

        url = response.request.url
        soup = BeautifulSoup(response.text, 'lxml')

        d = {}
        for element in soup.find_all():
            d["id"] = url
            if element.name.lower() in ["html", "body", "script", "footer", "style"]:
                pass

            else:
                x = element.find_all(text=True, recursive=False)
                if x:
                    if element.name.lower() not in ["title", "a", "p", "h1", "h2", "h3", "h4", "h5", "h6"]:
                        if "other_attributes" in d and d["other_attributes"] is not None:
                            d["other_attributes"].extend(x)
                        else:
                            d["other_attributes"] = x
                    else:
                        d[element.name.lower()] = x
        yield d
