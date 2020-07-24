# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class InstItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    user_parse_id = scrapy.Field()
    inst_id = scrapy.Field()
    photo_link = scrapy.Field()
    is_private = scrapy.Field()
    type = scrapy.Field()
    parse_user_name = scrapy.Field()

    pass
