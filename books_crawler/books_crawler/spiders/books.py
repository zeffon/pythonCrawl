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

# from scrapy.spiders import Spider
# from scrapy.http import Request
#
# def product_description(response, value):
#     return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract()[0]
#
# class BooksSpider(Spider):
#     name = 'books'
#     allowed_domains = ['books.toscrape.com']
#     start_urls = ['http://books.toscrape.com']
#     def parse(self, response):
#         books = response.xpath('//h3/a/@href').extract()
#         for book in books:
#             absolute_url = response.urljoin(book)
#             yield Request(absolute_url, callback=self.parse_book)
#         next_page_url = response.xpath('//a[text()="next"]/@href').extract()[0]
#         absolute_next_page_url = response.urljoin(next_page_url)
#         yield Request(absolute_next_page_url)
#     def parse_book(self, response):
#         title = response.css('h1::text').extract()[0]
#         price = response.xpath('//*[@class="price_color"]/text()').extract()[0]
#         image_url = response.xpath('//img/@src').extract()[0]
#         image_url = image_url.replace('../..', 'http://books.toscrape.com')
#         rating = response.xpath('//*[contains(@class,"star-rating")]/@class').extract()[0]
#         rating = rating.replace('star-rating', '')
#         description = response.xpath('//*[@id="product_description"]/following-sibling::p').extract()[0]
#         upc = product_description(response, 'UPC')
#         product_type = product_description(response, 'Product Type')
#         price_without_tax = product_description(response, 'Price (excl. tax)')
#         price_with_tax = product_description(response, 'Price (incl. tax)')
#         tax = product_description(response, 'Tax')
#         availability = product_description(response, 'Availability')
#         number_of_reviews = product_description(response, 'Number of reviews')

# import os
# import glob
# from scrapy.spiders import Spider
# from scrapy.http import Request
# from books_crawler.items import BooksCrawlerItem
#
# def product_description(response, value):
#     return response.xpath('//th[text()="' + value + '"]/following-sibling::td/text()').extract()[0]
#
# class BooksSpider(Spider):
#     name = 'books'
#     allowed_domains = ['books.toscrape.com']
#     start_urls = ['http://books.toscrape.com']
#     def parse(self, response):
#         books = response.xpath('//h3/a/@href').extract()
#         for book in books:
#             absolute_url = response.urljoin(book)
#             yield Request(absolute_url, callback=self.parse_book)
#         next_page_url = response.xpath('//a[text()="next"]/@href').extract()[0]
#         absolute_next_page_url = response.urljoin(next_page_url)
#         yield Request(absolute_next_page_url)
#     def parse_book(self, response):
#         items = BooksCrawlerItem()
#         title = response.css('h1::text').extract()[0]
#         price = response.xpath('//*[@class="price_color"]/text()').extract()[0]
#         image_url = response.xpath('//img/@src').extract()[0]
#         image_url = image_url.replace('../..', 'http://books.toscrape.com')
#         rating = response.xpath('//*[contains(@class,"star-rating")]/@class').extract()[0]
#         rating = rating.replace('star-rating', '')
#         description = response.xpath('//*[@id="product_description"]/following-sibling::p').extract()[0]
#         upc = product_description(response, 'UPC')
#         product_type = product_description(response, 'Product Type')
#         price_without_tax = product_description(response, 'Price (excl. tax)')
#         price_with_tax = product_description(response, 'Price (incl. tax)')
#         tax = product_description(response, 'Tax')
#         availability = product_description(response, 'Availability')
#         number_of_reviews = product_description(response, 'Number of reviews')
#
#         items['title'] = title
#         items['price'] = price
#         items['image_url'] = image_url
#         items['rating'] = rating
#         items['description'] = description
#         items['upc'] = upc
#         items['product_type'] = product_type
#         items['price_without_tax'] = price_without_tax
#         items['price_with_tax'] = price_with_tax
#         items['tax'] = tax
#         items['availability'] = availability
#         items['number_of_reviews'] = number_of_reviews
#
#         yield items
#
#     def close(self, reason):
#         csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
#         os.rename(csv_file, 'foovar.csv')

import os
import csv
import glob
import pymysql.cursors
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
        # next_page_url = response.xpath('//a[text()="next"]/@href').extract()[0]
        # absolute_next_page_url = response.urljoin(next_page_url)
        # yield Request(absolute_next_page_url)
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

        yield {
            'title': title,
            'rating': rating,
            'upc': upc,
            'product_type': product_type,
            'price_without_tax': price_without_tax,
            'price_with_tax': price_with_tax,
            'tax': tax,
            'availability': availability,
            'number_of_reviews': number_of_reviews
        }

    def close(self, reason):
        pass
        # csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)
        # connection = pymysql.connect(host='127.0.0.1',
        #                              user='root',
        #                              password='123456',
        #                              db='books_db',
        #                              charset='utf8mb4',
        #                              unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
        #                              cursorclass=pymysql.cursors.DictCursor)
        #
        #
        # try:
        #     with connection.cursor() as cursor, open(csv_file, 'r') as data_file:
        #         csv_data = csv.reader(data_file)
        #         row_count = 0
        #         for row in csv_data:
        #             print(row)
        #             if row_count != 0:
        #                 cursor.execute(
        #                     'insert ignore into books_table (title, rating, upc, product_type, price_without_tax,'
        #                     'price_with_tax, tax, availability, number_of_reviews) values (%s, %s, %s, %s, %s, %s,'
        #                     '%s, %s, %s)', row)
        #             row_count += 1
        #     connection.commit()
        # finally:
        #     connection.close()