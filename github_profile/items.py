# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class GithubLinkItem(scrapy.Item):
    # define the fields for your item here like:
    idx  = scrapy.Field()
    link = scrapy.Field()


class GithubProfileItem(scrapy.Item):
    # define the fields for your item here like:
    company = scrapy.Field()
    name = scrapy.Field()
    email = scrapy.Field()
    git_link = scrapy.Field()