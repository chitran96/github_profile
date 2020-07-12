# -*- coding: utf-8 -*-
import scrapy, json

from scrapy import Spider
from scrapy.selector import Selector

from github_profile.items import GithubProfileItem


class InfoSpider(scrapy.Spider):
    name = 'info'
    start_urls = []

    custom_settings = {'FEED_URI': 'result.json', 'CLOSESPIDER_TIMEOUT' : 15} # This will tell scrapy to store the scraped record to outputfile.json and for how long the spider should run.

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        with open('links.json') as json_file:
            for line in json_file:
                record = json.loads(line)
                self.start_urls.append(record['link']) 

    def parse(self, response):
        item = GithubProfileItem()
        item['name'] = Selector(response).xpath("//span[contains(@class, 'p-name')]/text()").get()
        item['company'] = Selector(response).xpath("//span[@class='p-org']/div/text()").get()
        item['email'] = Selector(response).xpath("//a[contains(@class,'u-email')]/text()").get()
        yield item