# -*- coding: utf-8 -*-
from scrapy.spider import Spider
import json

class ShowspiderSpider(Spider):
    name = 'showSpider'
    allowed_domains = ['www.olx.co.ke']
    start_urls = ['https://www.olx.co.ke/ajax/misc/contact/phone/15PcCi/>']

    def parse(self, response):
        body = response.body
        data = json.loads(body)
        print(data['value'])
