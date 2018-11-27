# -*- coding: utf-8 -*-
import logging
import multiprocessing
from datetime import datetime
from urllib import request

from bs4 import BeautifulSoup

from core.foundation.utils import date_utils
from core.foundation.utils.date_utils import Y_M_D, to_string, format_date
from core.repository.mongo_client import MongoClient

logger = logging.getLogger(__name__)


def export(currency_historical):
    return {
        'currency': currency_historical.currency,
        'open': currency_historical.open,
        'close': currency_historical.close,
        'high': currency_historical.high,
        'low': currency_historical.low,
        'volume': currency_historical.volume,
        'market_cap': currency_historical.market_cap,
        'date': currency_historical.date,
        'update_date': datetime.utcnow(),
    }


def save(currency_historical):
    found_currency_historical = mongo_client.collection('currencies_historical').find_one(
        {'currency': currency_historical.currency, 'date': currency_historical.date})
    if found_currency_historical is not None:
        logger.info(f'{found_currency_historical.currency} is already existed in {currency_historical.date}')
    else:
        mongo_client.collection('currencies_historical').insert_one(export(currency_historical))


def get_start_date(currency):
    currency_historical_list = list(mongo_client.collection('currencies_historical').find({'currency': currency}))
    if len(currency_historical_list) == 0:
        return '20130428'
    last_update_currency = currency_historical_list[0]
    return to_string(date_utils.add_date(last_update_currency.get('date'), Y_M_D), Y_M_D).replace('-', '')


class CurrencyHistorical(object):
    currency = date = open = high = low = close = volume = market_cap = None


def fetch_currency_historical(currency):
    root_url = 'https://coinmarketcap.com/currencies/'
    start_date = get_start_date(currency)
    update_date = date_utils.current(Y_M_D)
    url = root_url + currency + '/historical-data?start=' + start_date + '&end=' + update_date.replace('-', '')
    response = request.Request(url)
    if response is not None:
        page = request.urlopen(response).read()
        bsObj = BeautifulSoup(page, 'html.parser')
        trs = bsObj.tbody.find_all('tr', {'class': 'text-right'})
        for tr in trs:
            tds = tr.find_all('td')
            currency_historical = CurrencyHistorical()
            currency_historical.date = format_date(tds[0].get_text())
            currency_historical.open = float(tds[1]['data-format-value'])
            currency_historical.high = float(tds[2]['data-format-value'])
            currency_historical.low = float(tds[3]['data-format-value'])
            currency_historical.close = float(tds[4]['data-format-value'])
            currency_historical.volume = float(tds[5]['data-format-value'])
            currency_historical.market_cap = float(tds[6]['data-format-value'])
            currency_historical.currency = currency
            save(currency_historical)
        logger.info(f'{currency_historical.currency} historical data saved successfully.')


def fetch_currencies_historical():
    global mongo_client
    mongo_client = MongoClient()

    currencies = fetch_currencies()
    pool = multiprocessing.Pool(4)
    for currency in currencies:
        pool.apply_async(fetch_currency_historical, (currency,))
    pool.close()
    pool.join()

    mongo_client.close()


def fetch_currencies():
    url = 'https://coinmarketcap.com/all/views/all/'
    response = request.Request(url)
    page = request.urlopen(response).read()
    bsObj = BeautifulSoup(page, 'html.parser')
    spans = bsObj.tbody.find_all('span', {'class': 'currency-symbol'})
    currencies = []
    for span in spans:
        currency = span.find_all('a')[0]['href'].split('/')[2]
        currencies.append(currency)
    return currencies
