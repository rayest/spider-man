import logging
from datetime import datetime

from scrapy.conf import settings

from core.foundation.utils.date_utils import utc_date
from core.repository.mongo_client import MongoClient

logger = logging.getLogger(__name__)


class SpiderRepository():

    def __init__(self):
        self.mongo_client = MongoClient()

    def export(self, spider, data):
        return {
            'reference_no': spider.reference_no,
            'data': dict(data),
            'StandardUpdateTime': utc_date(spider.spider_start_time),
            'RealUpdateTime': datetime.utcnow(),
            'data_source': spider.market
        }

    def save_raw(self, spider, data):
        self.mongo_client.mongo_db = 'pan_gu'
        self.mongo_client.collection(spider.name).insert_one(self.export(spider, data))

    def save(self, spider, data):
        self.mongo_client.mongo_db = settings.get('MONGO_DB')
        document = self.mongo_client.collection(spider.name).find_one({'reference_no': spider.reference_no})
        if document is None:
            self.mongo_client.collection(spider.name).insert_one(self.export(spider, data))
        else:
            logger.info(f'reference_no {spider.reference_no} is already existed in {spider.market}:{spider.name}.')

    def close(self):
        self.mongo_client.close()
