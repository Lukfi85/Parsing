# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class LabirintRuSpider(scrapy.Spider):
    name = 'labirint_ru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/books/']

    def parse(self, response:HtmlResponse):

        next_page = response.xpath("//div[@class='pagination-next']/a/@href").extract_first()
        book_links = response.xpath("//div[@class='products-row ']//a[@class='product-title-link']/@href").extract()

        for link in book_links:
            yield response.follow(link, callback=self.book_parse)

        yield response.follow(next_page, callback=self.parse)


    def book_parse(self, response:HtmlResponse):
        title = response.xpath("//h1/text()").extract_first()
        authors = response.xpath("//div[@class='authors']/a/text()").extract_first()
        price = response.xpath("//span[@class='buying-price-val-number']/text()").extract_first()
        price_old = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        special_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        rate = response.xpath("//div[@id='rate']/text()").extract_first()
        link = response.url
        yield BookparserItem(title=title,
                             authors=authors,
                             price=price,
                             price_old=price_old,
                             special_price=special_price,
                             rate=rate,
                             link=link)




