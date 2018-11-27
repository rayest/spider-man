# -*- coding: utf-8 -*-
import logging

import requests

from core.foundation.utils import date_utils
from core.foundation.utils.date_utils import Y_M_D_H_M
from core.foundation.utils.generator import gen_reference_no
from core.repository.spider_repository import SpiderRepository

logger = logging.getLogger(__name__)


class TickerSpider():
    spider_start_time = reference_no = None

    name = 'ticker'
    market = 'coinmarketcap'

    def __init__(self):
        self.spider_start_time = date_utils.current(Y_M_D_H_M)
        self.spider_repository = SpiderRepository()

    def fetch_ticker(self):
        self.fetch()
        self.spider_repository.close()

    def fetch(self):
        for i in range(17):
            start = i * 100 + 1
            url = 'https://api.coinmarketcap.com/v2/ticker/?convert=BTC&limit=100&start=' + str(start)
            response = requests.get(url).json()
            num_cryptocurrencies = response.get('metadata').get('num_cryptocurrencies')
            data = response.get('data')
            if data is not None:
                self.spider_repository.save_raw(self, response)
                for key, value in data.items():
                    self.reference_no = gen_reference_no(url + value.get('name'))
                    self.spider_repository.save(self, value)
                logger.info(f'Ticker of currencies from No.{start} to No.{start + 99} saved. Total: {num_cryptocurrencies}')
