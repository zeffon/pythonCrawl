# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs

class MoviecrawlPipeline(object):
    def __init__(self):
        self.file = codecs.open(
            'movie_info.json', 'w', encoding='utf-8'
        )
    def process_item(self, item, spider):
        if spider.name == "":
            item['content'] = item['content'][-2]
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.file.write(line)
            return item
        else:
            print('name', type(item['name']), len(item['name']))
            print('pic', type(item['pic']), len(item['pic']))
            print('content', type(item['content']), len(item['content']))
            print('download', type(item['download']), len(item['download']))
            line = json.dumps(dict(item), ensure_ascii=False) + '\n'
            self.file.write(line)
    def spider_close(self, spider):
        self.file.close()