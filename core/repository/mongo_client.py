import logging
import pymongo
from scrapy.conf import settings


class MongoClient(object):
    def __init__(self):
        self.mongo_uri = settings.get('MONGO_URI')
        self.mongo_db = settings.get('MONGO_DB')
        self.client = pymongo.MongoClient(self.mongo_uri, connect=False)
        logging.info("MongoDB client created.")

    def collection(self, collection_name):
        return self.client[self.mongo_db][collection_name]

    def mqcollection(self):
        return self.client[self.mongo_db]['rabbitmq']

    def close(self):
        logging.info("MongoDB connection is closed.")
        self.client.close()
