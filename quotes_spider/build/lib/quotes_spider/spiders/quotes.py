# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ..items import QuotesSpiderItem
from scrapy.loader import ItemLoader

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        l = ItemLoader(item=QuotesSpiderItem(), response=response)
        h1_tag = response.xpath('//h1/a/text()').extract()[0]
        tags = response.xpath('//*[@class="tag-item"]/a/text()').extract()
        l.add_value('h1_tag', h1_tag)
        l.add_value('tags', tags)
        return l.load_item()
        # quotes = response.xpath('//*[@class="quote"]')
        # for quote in quotes:
        #     text = quote.xpath('.//*[@class="text"]/text()').extract()[0]
        #     author = quote.xpath('.//*[@itemprop="author"]/text()').extract()[0]
        #     # content = quote.xpath('.//*[@itemprop="keywords"]/@content').extract()[0]
        #     tags = quote.xpath('.//*[@class="tag"]/text()').extract()
        #     yield {
        #         'text': text,
        #         'author': author,
        #         'tags': tags
        #     }
        # next_page_url = response.xpath('//*[@class="next"]/a/@href').extract()[0]
        # absolue_next_page_url = response.urljoin(next_page_url)
        # yield Request(absolue_next_page_url, callback=self.parse)


