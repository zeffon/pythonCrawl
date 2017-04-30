# -*- coding: utf-8 -*-
import scrapy


class NikespiderSpider(scrapy.Spider):
    name = 'nikeSpider'
    allowed_domains = ['nike.com']
    start_urls = ['http://store.nike.com/us/en_us/pd/magista-opus-ii-tech-craft-2-mens-firm-ground-soccer-cleat/pid-11229710/pgid-11918119']

    def parse(self, response):
        sizes = response.xpath('//*[@class="nsg-form--drop-down exp-pdp-size-dropdown exp-pdp-dropdown two-column-dropdown"]/option')
        print(sizes)
        for s in sizes:
            size = s.xpath('text()[not(parent::option/@class="exp-pdp-size-not-in-stock selectBox-disabled")]').extract_first('').strip()
