# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Book24RuSpider(scrapy.Spider):
    name = 'book24_ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/catalog/khudozhestvennaya-literatura-dlya-detey-1160/']

    def parse(self, response):

        next_page = response.css("a.catalog-pagination__item._text.js-pagination-catalog-item::attr(href)").extract()[-1]


        book_links = response.css("a.book__title-link.js-item-element.ddl_product_link ::attr(href)").extract()

        for link in book_links:
            yield response.follow(link, callback=self.book_parse)

        yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response:HtmlResponse):
        title = response.xpath("//h1/text()").extract_first()
        authors = response.xpath("//div[@class='item-tab__chars-list']//a/text()").extract_first()
        price = response.xpath("//div[@class='item-actions__price']/b/text()").extract_first()
        price_old = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        special_price = response.xpath("//div[@class='item-actions__price']/b/text()").extract_first()
        rate = response.xpath("//span[@class='rating__rate-value']/text()").extract_first()
        link = response.url
        yield BookparserItem(title=title,
                             authors=authors,
                             price=price,
                             price_old=price_old,
                             special_price=special_price,
                             rate=rate,
                             link=link)




