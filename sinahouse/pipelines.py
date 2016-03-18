# -*- coding: utf-8 -*-



# import utils
# import MySQLdb 
import threading
import logging
import pymongo
import scrapy  
from scrapy.mail import MailSender 
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
import requests
from utils import semaphore_thread

logging.getLogger("requests").setLevel(logging.WARNING)

class MongoPipeline(object):
    
    def __init__(self, settings):
        self.settings = settings
        self.client = pymongo.MongoClient(host=settings.get('MONGO_HOST'), port=settings.get('MONGO_PORT'))
        self.db = self.client[settings.get('MONGO_DATABASE')]
        self.collection = settings.get('MONGO_COLLECTION')
                
    @classmethod
    def from_crawler(cls, crawler):
        return cls(settings = crawler.settings)
    
    def process_item(self, item, spider):
        self.db[self.collection].insert_one(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()
#         mailer = MailSender.from_settings(self.settings)        
#         mailer.send(to=["lingang@xxx.com"], subject="THANKS", body="THANKS YOU!",cc=[])