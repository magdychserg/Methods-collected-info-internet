# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient

class InstaparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.insta

    def process_item(self, item, spider):
        collection = self.db[item['_collection']]
        collection.save(item)
        return item

