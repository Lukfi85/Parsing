# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def clean_spec_val(value):
    return ' '.join(value.replace('\n', '').split())

def clean_price(value):
    return int(value.replace(' ',''))


class LeroymerlinItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(clean_price))
    spec = scrapy.Field()
    spec_val = scrapy.Field(input_processor=MapCompose(clean_spec_val))

