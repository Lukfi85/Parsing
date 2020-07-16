# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from LEROYMERLIN.items import LeroymerlinItem
from scrapy.loader import ItemLoader

class LeroymerlinruSpider(scrapy.Spider):
    name = 'LEROYMERLINRU'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/catalogue/dreli/']

    def parse(self, response:HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        staff_links = response.xpath("//a[@class='black-link product-name-inner']/@href").extract()
        for link in staff_links:
            yield response.follow(link,callback=self.parse_staff)
        yield response.follow(next_page,callback=self.parse)

    def parse_staff(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroymerlinItem(), response=response)
        loader.add_xpath('name', "//h1/text()" )
        loader.add_xpath('photos', "//source[@media=' only screen and (min-width: 1024px)']/@srcset")
        loader.add_value('url', response.url)
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('spec', "//dt/text()")
        loader.add_xpath('spec_val', "//dd/text()")


        yield loader.load_item()


