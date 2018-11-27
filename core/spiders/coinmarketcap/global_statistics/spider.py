# -*- coding: utf-8 -*-
import json
import logging

from core.spiders.spider_man import SpiderMan

from .item import GlobalItem

logger = logging.getLogger(__name__)


class GlobalSpider(SpiderMan):
    name = 'global_statistics'
    allowed_domains = ['coinmarketcap.com']
    url = 'https://s2.coinmarketcap.com/generated/stats/global.json'
    market = 'coinmarketcap'
    custom_settings = {
        'ITEM_PIPELINES': {
            'core.pipelines.RepositoryPipeline': 2
        }
    }

    def parse(self, response):
        logger.info('Global spider is running...')
        json_response = json.loads(response.body_as_unicode())
        item = GlobalItem()
        item["active_cryptocurrencies"] = json_response["active_cryptocurrencies"]
        item["active_markets"] = json_response["active_markets"]
        item["bitcoin_percentage_of_market_cap"] = json_response["bitcoin_percentage_of_market_cap"]
        item["total_market_cap_by_available_supply_usd"] = json_response["total_market_cap_by_available_supply_usd"]
        item["total_volume_usd"] = json_response["total_volume_usd"]
        yield item
