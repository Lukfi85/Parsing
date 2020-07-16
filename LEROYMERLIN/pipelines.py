# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

# from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient
import os
from urllib.parse import urlparse
from scrapy.pipelines.files import FilesPipeline


class DataBasePipeline:
    def __init__(self):
        self.client = MongoClient('localhost',27017)
        self.mongo_base = self.client.leroymerlin
    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item
    def __del__(self):
        self.client.close()


class LeroymerlinSpecPipeline:
    def process_item(self, item, spider):
        data = {}
        item['price'] = item['price'][0]
        for ind, i in enumerate(item['spec']):
            data[i]=item['spec_val'][ind]
        item['spec'] = data
        del item['spec_val']

        return item


class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img,meta=item)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=True):
        way = 'full/'
        folder = request.meta['name']
        return f'{way}{folder}/' + os.path.basename(urlparse(request.url).path)


    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item



