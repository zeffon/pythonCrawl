# -*- coding: utf-8 -*-
import scrapy


class ZhihuspiderSpider(scrapy.Spider):
    name = "zhihuSpider"
    allowed_domains = ["www.olx.co.ke"]
    start_urls = ['https://www.olx.co.ke/ad/private-tutors-and-home-tuition-services-ID15PcCi.html']

    def parse(self, response):
        pass
