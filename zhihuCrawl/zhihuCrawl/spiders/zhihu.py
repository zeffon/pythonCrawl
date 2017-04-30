# -*- coding: utf-8 -*-
# from scrapy.spiders import Spider
from scrapy_redis.spiders import RedisSpider

class ZhihuSpider(RedisSpider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/question/32302268']
    redis_key = 'ZhihuSpider:start_urls'

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(ZhihuSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        return {
            'url': response.url
        }
