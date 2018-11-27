import logging
import threading
import time
from datetime import datetime
from multiprocessing import Process

import schedule
from scrapy.crawler import CrawlerProcess

from core.spiders.ccxt_spiders.tickers import TickersFetcher
from core.spiders.coinmarketcap.currencies_historical.spider import fetch_currencies_historical
from core.spiders.coinmarketcap.global_statistics.spider import GlobalSpider
from core.spiders.coinmarketcap.ticker.ticker import TickerSpider

logger = logging.getLogger(__name__)


def run_global_spider():
    logger.info('Running....\n {}'.format(datetime.now()))
    crawler_process = CrawlerProcess()
    crawler_process.crawl(GlobalSpider)
    crawler_process.start(stop_after_crawl=True)


def global_job():
    logger.info('Running....\n {}'.format(datetime.now()))
    process = Process(target=run_global_spider)
    process.start()


def currencies_historical_job():
    logger.info('Running....\n {}'.format(datetime.now()))
    process = Process(target=fetch_currencies_historical)
    process.start()


def tickers_job():
    logger.info('Running....\n {}'.format(datetime.now()))
    ticker_spider = TickersFetcher()
    ticker_spider.get_tickers()
    # process = Process(target=ticker_spider.get_tickers)
    # process.start()


def ticker_job():
    logger.info('Running....\n {}'.format(datetime.now()))
    ticker_spider = TickerSpider()
    ticker_spider.fetch_ticker()
    # process = Process(target=ticker_spider.fetch_ticker)
    # process.start()


def run():
    threads = []
    t1 = threading.Thread(target=ticker_job)
    t2 = threading.Thread(target=tickers_job)
    t3 = threading.Thread(target=global_job)
    t4 = threading.Thread(target=currencies_historical_job)
    threads.append(t1)
    threads.append(t2)
    threads.append(t3)
    threads.append(t4)
    for thr in threads:
        thr.start()
    for thr in threads:
        if thr.isAlive():
            thr.join()

    schedule.every(1).second.do(tickers_job)
    schedule.every(4).minutes.do(global_job)
    schedule.every().day.at('10:10').do(currencies_historical_job)
    schedule.every(4).minutes.do(ticker_job)

    while True:
        if int(time.time()) % 60 == 0:
            schedule.run_pending()
        time.sleep(1)
