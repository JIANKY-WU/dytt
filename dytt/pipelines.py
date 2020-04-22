# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class DyttPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPiline():
    def __init__(self,host):
        self.host=host

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host=crawler.settings.get('HOST'),
        )
    def open_spider(self,spider):
        self.client=pymongo.MongoClient(host=self.host)
        self.collection=self.client.test.my

    def process_item(self,item,spider):
        self.collection.insert({"url":item['movie_url']})
        return item

