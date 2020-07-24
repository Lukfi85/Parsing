# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import os
from urllib.parse import urlparse
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline
import scrapy


class InstPipeline:
    def __init__(self):
        self.client = MongoClient('localhost',27017)
        self.mongo_base = self.client.inst

    def process_item(self, item, spider):
        collection = self.mongo_base[item['parse_user_name']]
        collection.insert_one(item)
        return item

    def __del__(self):
        self.client.close()


class Instaphoto(ImagesPipeline):
    def get_media_requests(self, item, info):
            try:
                yield scrapy.Request(item['photo_link'],meta=item)
            except Exception as e:
                print(e)

    def file_path(self, request, response=None, info=True):
        way = 'full/'
        folder = request.meta['parse_user_name']
        return f'{way}{folder}/' + os.path.basename(urlparse(request.url).path)


    def item_completed(self, results, item, info):

        if results:
            item['photo_link'] = [itm[1] for itm in results if itm[0]]
        return item

