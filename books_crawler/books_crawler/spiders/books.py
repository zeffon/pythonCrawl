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
import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from selenium import webdriver
from scrapy.http import Request
from selenium.common.exceptions import NoSuchElementException
from time import sleep

class BooksSpider(Spider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    def start_requests(self):
        self.driver = webdriver.Chrome('/Users/yuzefeng/Documents/Tools/python/chromedriver')
        self.driver.get('http://books.toscrape.com')
        sel = Selector(text=self.driver.page_source)
        books = sel.xpath('//h3/a/@href').extract()
        for book in books:
            url = 'http://books.toscrape.com/' + book
            yield Request(url, callback=self.parse_book)
        while True:
            try:
                element = self.driver.find_element_by_xpath('//a[text()="next"]')
                sleep(3)
                self.logger.info('sleep 3 seconds')
                element.click()
                sel = Selector(text=self.driver.page_source)
                books = sel.xpath('//h3/a/@href').extract()
                for book in books:
                    url = 'http://books.toscrape.com/catalogue/' + book
                    yield Request(url, callback=self.parse_book)
            except NoSuchElementException:
                self.logger.info('No Such ElementException')
                self.driver.quit()
                break
    def parse_book(self, response):
        pass