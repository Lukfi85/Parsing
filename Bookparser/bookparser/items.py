# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    title = scrapy.Field()
    authors = scrapy.Field()
    price_old = scrapy.Field()
    special_price = scrapy.Field()
    price = scrapy.Field()
    rate = scrapy.Field()
    link = scrapy.Field()
