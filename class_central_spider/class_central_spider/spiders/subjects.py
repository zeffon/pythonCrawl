# -*- coding: utf-8 -*-
from scrapy.spider import Spider
from scrapy.http import Request


class SubjectsSpider(Spider):

    name = 'subjects'
    allowed_domains = ['class-central.com']
    start_urls = ['http://class-central.com/subjects']

    def __init__(self, subject=None):
        self.subject = subject
    def parse_subject(self, response):
        subject_names = response.xpath('//title/text()').extract()[0].split(' | ')
        subject_name = subject_names[0]
        courses = response.xpath('//*[@class="course-name"]')
        for course in courses:
            course_name = course.xpath('.//@title').extract()[0]
            course_url = course.xpath('.//@href').extract()[0]
            absolute_course_url = response.urljoin(course_url)
            yield {
                'subject_name': subject_name,
                'course_name': course_name,
                'absolute_course_url': absolute_course_url
            }
        next_page = response.xpath('//*[@rel="next"]/@href').extract()[0]
        absolut_next_page_url = response.urljoin(next_page)
        yield Request(absolut_next_page_url, callback=self.subject)
    def parse(self, response):
        if self.subject:
            subject_url = response.xpath('//*[contains(@title, "' + self.subject + '")]/@href').extract()[0]
            url = response.urljoin(subject_url)
            yield Request(url, callback=self.parse_subject)
        else:
            self.logger.info('Scraping all subjects.')
            self.subject = 'show-all-subjects view-all-courses'
            subject_urls = response.xpath('//*[contains(@class, "' + self.subject + '")]/@href').extract()
            for url in subject_urls:
                url = response.urljoin(url)
                yield Request(url, callback=self.parse_subject)
