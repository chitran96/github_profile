# -*- coding: utf-8 -*-
import scrapy, os

from scrapy import Spider
from scrapy.selector import Selector
from github_profile.items import GithubLinkItem 


class LinkSpider(scrapy.Spider):
    name = 'link'
    start_urls = []
    
    custom_settings =   {
                            'FEEDS': {
                                'links.json': {
                                    'format': 'jsonlines'
                                },
                            }, 
                            'CLOSESPIDER_TIMEOUT' : 60
                        } # This will tell scrapy to store the scraped record to outputfile.json and for how long the spider should run.
    def __init__(self, category=[], name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.start_urls = category
        if os.path.exists("links.json"): 
            os.remove("links.json")
        print("LinkSpider init")

    def parse(self, response):
        names = Selector(response).xpath("//a[@class='mr-1']")
        for name in names:
            link = self.start_urls[0] + name.xpath("@href").get()
            yield GithubLinkItem(link=link)
