# -*- coding: utf-8 -*-
import scrapy, json, os
from scrapy.http import Request

from scrapy import Spider
from scrapy.selector import Selector
from scrapy import signals


from github_profile.items import GithubProfileItem


class InfoSpider(scrapy.Spider):
    name = 'info'
    start_urls = ["https://github.com/login"]
    custom_settings =   {
                            'FEEDS': {
                                'items.csv': {
                                    'format': 'csv',
                                    'fields': ['name', 'company', 'email', 'git_link'],
                                },
                            }, 
                            'CLOSESPIDER_TIMEOUT' : 60
                        } # This will tell scrapy to store the scraped record to outputfile.json and for how long the spider should run.

    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        if os.path.exists("items.csv"): 
            os.remove("items.csv")
        print("InfoSpider init")
        self.start_urls[1:] = []

    def parse_something(self, response):
        item = GithubProfileItem()
        item['git_link'] = response._get_url()
        item['name'] = Selector(response).xpath("//span[contains(@class, 'p-name')]/text()").get()
        item['company'] = Selector(response).xpath("//span[@class='p-org']/div/text()").get()
        item['email'] = Selector(response).xpath("//a[contains(@class,'u-email')]/text()").get()
        yield item

    def after_login(self, response):
        with open('links.json') as json_file:
            for line in json_file:
                record = json.loads(line)
                self.start_urls.append(record['link']) 
        print(self.start_urls)

        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_something)

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'login': 'username', 'password': 'password'},
            callback=self.after_login
        )
