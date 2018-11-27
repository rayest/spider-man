# -*- coding: utf-8 -*-
import logging

from core.repository.spider_repository import SpiderRepository

logger = logging.getLogger(__name__)


class RepositoryPipeline():
    def process_item(self, item, spider):
        self.spider_repository = SpiderRepository()
        self.spider_repository.save(spider, item)
        return item


class MQPipeline():
    def process_item(self, item, spider):
        self.spider_repository = SpiderRepository()
        self.collection = spider.mongo_client.mqcollection()
        self.spider_repository.save(spider, item)
        return item
