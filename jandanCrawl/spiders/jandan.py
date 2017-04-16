import scrapy
from ..items import JandancrawlItem
class jandanSpider(scrapy.Spider):
    name = "jandan"
    allow_domains = ["http://jandan.net/"]
    start_urls = ["http://jandan.net"]
    def parse_info(self, response):
        url = response.xpath('//div[@class="post f"]/h1/a/@href').extract()
        name = response.xpath('//div[@class="post f"]/h1/a/text()').extract()
        item = response.meta['jandan']
        item['name'] = name
        item['url'] = url
        return item
    def parse_page(self, response):
        urls = response.xpath('//div[@class="post"]/div[@class="thumbs_b"]/a/@href').extract()
        print(urls)
        for url in urls:
            jandan = JandancrawlItem()
            yield scrapy.Request(
                url,
                meta={'jandan': jandan},
                callback=self.parse_info
            )
    def parse(self, response):
        pageText = response.xpath('//div[@class="wp-pagenavi"]/span[@class="pages"]/text()').extract()
        pageCount = pageText[0].split('/')[-1]
        pageCount = int(pageCount.replace(',', ''))
        hostUrl = response.url + '/page/{}'
        for i in range(1, pageCount + 1):
            url = hostUrl.format(i)
            yield scrapy.Request(url, callback=self.parse_page)


