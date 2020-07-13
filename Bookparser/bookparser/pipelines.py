# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class BookparserPipeline(object):
    def __init__(self):
        self.client = MongoClient('localhost',27017)
        self.mongo_base = self.client.books

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)

        return item

    def __del__(self):
        self.client.close()