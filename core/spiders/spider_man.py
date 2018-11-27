# -*- coding: utf-8 -*-
import logging

import scrapy
from core.foundation.utils import date_utils, generator
from core.foundation.utils.date_utils import Y_M_D_H_M
from core.repository.mongo_client import MongoClient

logger = logging.getLogger(__name__)


class SpiderMan(scrapy.Spider):
    spider_start_time = mongo_client = url = collection = mqcollection = reference_no = None

    custom_settings = {
        'ITEM_PIPELINES': {
            'core.pipelines.RepositoryPipeline': 50,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'core.middlewares.UserAgent': 1,
            'core.middlewares.HttpProxy': 3,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 2,
        },
        'COOKIES_ENABLED': False,
        # important
        'DOWNLOAD_TIMEOUT': 30

    }

    def start_requests(self):
        logger.info('Spider [{}] is starting... '.format(self.name))
        logger.info('{} is to be crawled'.format(self.url))
        self.reference_no = self.gen_reference_no(self.url)

        self.mongo_client = MongoClient()
        self.collection = self.mongo_client.collection(self.name)

        document = self.collection.find_one({"reference_no": self.reference_no})
        if document is not None:
            logger.info(f'{self.reference_no} is already existed.')
            return

        self.spider_start_time = date_utils.current(Y_M_D_H_M)
        yield scrapy.Request(self.url, self.parse)

    def gen_reference_no(self, url):
        return generator.gen_reference_no(url)

    def closed(self, reason):
        logger.info('Spider [{}] is closed. '.format(self.name))
        logger.info('Mongo connection for spider [{}] is ready to close.'.format(self.name))
        self.mongo_client.close()
