# coding=utf-8
import logging
import os
from logging.handlers import RotatingFileHandler
from time import strftime
from urllib.parse import quote

from scrapy.conf import settings


class BasicConfig:
    LOG_PATH = 'logs'
    MONGO_USER = ''
    MONGO_PASSWORD = ''
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = '27017'
    MONGO_DB = 'spider_man'
    MQ_HOST = '10.211.55.3'
    MQ_PORT = '5672'
    MQ_USER = 'admin'
    MQ_PASSWORD = 'admin'

    @classmethod
    def init_config(self, command_args):
        if command_args.log_path is not None:
            self.LOG_PATH = command_args.log_path
        self.config_logging(self.LOG_PATH)
        self.config_scrapy()

    @classmethod
    def config_scrapy(self):
        settings['MONGO_URI'] = 'mongodb://{}:{}@{}:{}'.format(self.MONGO_USER, quote(self.MONGO_PASSWORD),
                                                               self.MONGO_HOST, self.MONGO_PORT)
        settings['MONGO_DB'] = self.MONGO_DB
        settings['LOG_ENABLED'] = self.MONGO_DB
        settings['MQ_HOST'] = self.MQ_HOST
        settings['MQ_PORT'] = self.MQ_PORT
        settings['MQ_USER'] = self.MQ_USER
        settings['MQ_PASSWORD'] = self.MQ_PASSWORD
        settings['LOG_ENABLED'] = False

    def config_logging(log_path):
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        if not log_path.endswith('/'):
            log_path += '/'

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(threadName)s - %(thread)d - %(name)s - %(levelname)s - %(message)s')

        default_handler = RotatingFileHandler(strftime(log_path + 'log.%Y_%m_%d'), maxBytes=1024 * 1024 * 5,
                                              backupCount=100)
        default_handler.setLevel(logging.INFO)
        default_handler.setFormatter(formatter)
        logger.addHandler(default_handler)

        error_handler = RotatingFileHandler(strftime(log_path + 'error.log.%Y_%m_%d'), maxBytes=1024 * 1024 * 5,
                                            backupCount=100)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        logger.addHandler(error_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)
