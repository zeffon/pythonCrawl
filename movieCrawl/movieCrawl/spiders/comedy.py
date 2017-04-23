import scrapy
import re
import urllib
from ..items import MoviecrawlItem
class movie87_spider(scrapy.Spider):
    name = "comedy"
    allowed_domains = ["www.87movie.com"]
    start_urls = ["http://www.87movie.com/tag/喜剧/"]
    def parse_info(self, response):
        movie_info = response.meta['movie_info']
        movie_info['name'] = response.xpath('//div[@class="white-div"]//h3/text()').extract()
        movie_info['pic'] = response.xpath('//div[@class="white-div"]//img/@src').extract()
        movie_info['content'] = response.xpath('//div[@class="white-div"]//div[@class="col-md-8"]/text()').extract()
        movie_info['download'] = response\
            .xpath('//div[@id="down1"]/div[@class="panel-body"]/ul/li/a/@href')\
            .extract()
        return movie_info
    def parse_page(self, response):
        movies = response.xpath('//ul[@class="list-unstyled mlist"]/li//h4/a/@href').extract()
        url_host = 'http://' + response.url.split('/')[2]
        for i in movies:
            movie_info = MoviecrawlItem()
            yield scrapy.Request(url_host + i, meta={'movie_info': movie_info}, callback=self.parse_info)

    def parse(self, response):
        print(response)
        num_page = response.xpath('//ul[@class="pagination"]//li[last()]/a/@href').extract()
        number = 1
        if len(num_page) > 0:
            number = int(num_page[0].split('/')[-1].split('?')[0])
        for i in range(1, number+1):
            target_url = response.url + str(i) + '?o=data'
            yield scrapy.Request(target_url, callback=self.parse_page)

