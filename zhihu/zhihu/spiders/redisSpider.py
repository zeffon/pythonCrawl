# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider


class redisSpider(RedisSpider):
    name = "redisSpider"
    allowed_domains = ["www.olx.co.ke"]
    start_urls = ['https://www.olx.co.ke/ad/private-tutors-and-home-tuition-services-ID15PcCi.html']

    def parse(self, response):
        print(response.url)
