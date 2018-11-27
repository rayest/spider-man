from scrapy.http import HtmlResponse

from core.spiders.coinmarketcap.global_statistics.spider import GlobalSpider
from tests.base_test import BaseTest


class GlobalSpiderTest(BaseTest):

    def test_parse(self):
        global_spider = GlobalSpider()
        response = self.session.get(global_spider.url)
        scrapy_response = HtmlResponse(body=response.content, url=global_spider.url)
        item = next(global_spider.parse(scrapy_response))
        self.assertIsNotNone(item)
        self.assertIsInstance(item.get('active_cryptocurrencies'), int)
        self.assertIsInstance(item.get('active_markets'), int)
        self.assertIsInstance(item.get('bitcoin_percentage_of_market_cap'), float)
        self.assertIsInstance(item.get('total_market_cap_by_available_supply_usd'), float)
        self.assertIsInstance(item.get('total_volume_usd'), float)
