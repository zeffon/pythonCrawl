import scrapy
from ..items import MoviecrawlItem
class db_movie(scrapy.Spider):
    name = "douban_movie"
    allowed_domains = ["movie.douban.com"]
    start_urls = ["http://movie.douban.com/later/beijing/"]
    def parse_info(self, response):
        movie_info = MoviecrawlItem()
        movie_info['name'] = response.xpath("//div[@id='content']/h1/span/text()").extract()
        movie_info['pic'] = response.xpath("//div[@id='mainpic']/a/img/@src").extract()
        movie_info['content'] = response.xpath("//div[@id='link-report']/span/text()").extract()
        movie_info['download'] = ""
        return movie_info
    def parse(self, response):
        movie_links = response.xpath('//div[@id="showing-soon"]/div/div/h3/a/@href').extract()
        for i in movie_links:
            yield scrapy.Request(i, callback=self.parse_info)