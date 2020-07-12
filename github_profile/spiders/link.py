# -*- coding: utf-8 -*-
import scrapy

from scrapy import Spider
from scrapy.selector import Selector
from github_profile.items import GithubLinkItem 


class LinkSpider(scrapy.Spider):
    name = 'link'
    start_urls = []
    custom_settings = {'FEED_URI': 'links.json', 'CLOSESPIDER_TIMEOUT' : 15} # This will tell scrapy to store the scraped data to outputfile.json and for how long the spider should run.

    def __init__(self, category=[], name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.start_urls = category

    def parse(self, response):
        names = Selector(response).xpath("//a[@class='mr-1']")
        for name in names:
            link = self.start_urls[0] + name.xpath("@href").get()
            yield GithubLinkItem(link=link)