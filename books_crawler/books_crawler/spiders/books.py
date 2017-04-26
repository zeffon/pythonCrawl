# -*- coding: utf-8 -*-
# import scrapy
# from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
#
# class BooksSpider(CrawlSpider):
#     name = "books"
#     allowed_domains = ["books.toscrape.com"]
#     start_urls = ['http://books.toscrape.com/']
#     rules = (Rule(LinkExtractor(), callback='parse_page', follow=False),)
#     def parse_page(self, response):
#         yield {'URL': response.url}


# import scrapy
# from scrapy.spiders import Spider
# from scrapy.selector import Selector
# from selenium import webdriver
# from scrapy.http import Request
# from selenium.common.exceptions import NoSuchElementException
# from time import sleep
#
# class BooksSpider(Spider):
#     name = 'books'
#     allowed_domains = ['books.toscrape.com']
#     def start_requests(self):
#         self.driver = webdriver.Chrome('/Users/yuzefeng/Documents/Tools/python/chromedriver')
#         self.driver.get('http://books.toscrape.com')
#         sel = Selector(text=self.driver.page_source)
#         books = sel.xpath('//h3/a/@href').extract()
#         for book in books:
#             url = 'http://books.toscrape.com/' + book
#             yield Request(url, callback=self.parse_book)
#         while True:
#             try:
#                 element = self.driver.find_element_by_xpath('//a[text()="next"]')
#                 sleep(3)
#                 self.logger.info('sleep 3 seconds')
#                 element.click()
#                 sel = Selector(text=self.driver.page_source)
#                 books = sel.xpath('//h3/a/@href').extract()
#                 for book in books:
#                     url = 'http://books.toscrape.com/catalogue/' + book
#                     yield Request(url, callback=self.parse_book)
#             except NoSuchElementException:
#                 self.logger.info('No Such ElementException')
#                 self.driver.quit()
#                 break
#     def parse_book(self, response):
#         pass
import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request

def product_description(response, value):
    return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract()[0]

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']
    def parse(self, response):
        books = response.xpath('//h3/a/@href').extract()
        for book in books:
            absolute_url = response.urljoin(book)
            yield Request(absolute_url, callback=self.parse_book)
        next_page_url = response.xpath('//a[text()="next"]/@href').extract()[0]
        absolute_next_page_url = response.urljoin(next_page_url)
        yield Request(absolute_next_page_url)
    def parse_book(self, response):
        title = response.css('h1::text').extract()[0]
        price = response.xpath('//*[@class="price_color"]/text()').extract()[0]
        image_url = response.xpath('//img/@src').extract()[0]
        image_url = image_url.replace('../..', 'http://books.toscrape.com')
        rating = response.xpath('//*[contains(@class,"star-rating")]/@class').extract()[0]
        rating = rating.replace('star-rating', '')
        description = response.xpath('//*[@id="product_description"]/following-sibling::p').extract()[0]
        upc = product_description(response, 'UPC')
        product_type = product_description(response, 'Product Type')
        price_without_tax = product_description(response, 'Price (excl. tax)')
        price_with_tax = product_description(response, 'Price (incl. tax)')
        tax = product_description(response, 'Tax')
        availability = product_description(response, 'Availability')
        number_of_reviews = product_description(response, 'Number of reviews')


