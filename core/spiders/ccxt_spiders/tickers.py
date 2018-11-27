import asyncio
import logging

import ccxt.async as ccxt
from ccxt.base.errors import RequestTimeout, DDoSProtection

from core.foundation.utils import date_utils, generator
from core.foundation.utils.date_utils import Y_M_D_H_M_S, Y_M_D_H_M
from core.repository.spider_repository import SpiderRepository
from core.spiders.ccxt_spiders.market_utils import markets_tickers_urls
from core.spiders.spider import Spider

logger = logging.getLogger(__name__)

USER_AGENT = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36(KHTML, likeGecko) Chrome/65.0.3325.181 Mobile Safari/537.36',


class TickersFetcher():

    def __init__(self):
        self.spider_repository = SpiderRepository()

    async def fetch_tickers(self, exchange):
        retries = 0
        while retries < 10:
            retries += 1
            try:
                logger.info(f'Try to fetch {exchange.id} for {retries} retries.')
                tickers = await exchange.fetch_tickers()
                await exchange.close()
                return tickers, retries
            except RequestTimeout as e:
                logger.error(f'{exchange.id} has an error: {type(e).__name__}')
                await asyncio.sleep(2)
            except DDoSProtection as e:
                logger.error(f'{exchange.id} has an error: {type(e).__name__}')
                await asyncio.sleep(5)
            except Exception as e:
                logger.error(f'{exchange.id} has an error: {type(e).__name__}')
                await asyncio.sleep(2)

    async def fetch_tickers_task(self, exchange):
        start_time = date_utils.current(Y_M_D_H_M)
        market = exchange.id
        ticker_url = markets_tickers_urls.get(market)
        reference_no = generator.gen_reference_no(ticker_url)

        tickers, retries = await self.fetch_tickers(exchange)
        if not tickers:
            logger.info(f'Tickers of {market} is given up fetching after 10 retries.')
            return
        logger.info(f'Tickers of {market} fetched after {retries} retries.')
        uniformed_tickers = {}
        for currency_pairs in tickers.keys():
            uniformed_tickers['t' + currency_pairs] = tickers.get(currency_pairs)

        spider = Spider().build_from(market, 'tickers', start_time, reference_no)
        self.spider_repository.save(spider, uniformed_tickers)
        logger.info(f'Tickers of {spider.market} saved.')
        return uniformed_tickers

    def get_tickers(self):
        logger.info('Ready to fetch tickers tasks....\n' + date_utils.current(Y_M_D_H_M_S))
        exchanges = [
            ccxt.bitfinex2({'userAgent': USER_AGENT}),
            ccxt.bittrex({'userAgent': USER_AGENT}),
            ccxt.poloniex({'userAgent': USER_AGENT}),
            ccxt.hitbtc2({'userAgent': USER_AGENT}),
            ccxt.cryptopia({'userAgent': USER_AGENT}),
            ccxt.livecoin({'userAgent': USER_AGENT}),
            ccxt.kucoin({'userAgent': USER_AGENT}),
            ccxt.okex({'userAgent': USER_AGENT}),
            ccxt.coinexchange({'userAgent': USER_AGENT}),
            ccxt.binance({'userAgent': USER_AGENT}),
            ccxt.bithumb({'userAgent': USER_AGENT}),
            ccxt.kraken({'userAgent': USER_AGENT})
        ]
        tasks = []
        for i in range(len(exchanges)):
            task = self.fetch_tickers_task(exchanges[i])
            tasks.append(asyncio.ensure_future(task))

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()
        self.spider_repository.close()
