# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# from openpyxl import Workbook
#
# class BooksCrawlerPipeline(object):
#     wb = Workbook()
#     ws = wb.active
#     ws.append(['Book Title', 'Price', 'Image URL', 'Rating', 'Description', 'UPC','Type', 'Price without Tax', 'Price with Tax', 'Tax', 'Availability','Number of Reviews'])
#     def process_item(self, item, spider):
#         line = [
#             item['title'],
#             item['price'],
#             item['image_url'],
#             item['rating'],
#             item['description'],
#             item['upc'],
#             item['product_type'],
#             item['price_without_tax'],
#             item['price_with_tax'],
#             item['tax'],
#             item['availability'],
#             item['number_of_reviews']
#         ]
#         self.ws.append(line)
#         self.wb.save('./books_crawler/result-excel.xlsx')
#         return item
from pymongo import MongoClient
from scrapy.conf import settings

class MongoDBPipeline(object):
    def __init__(self):
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item