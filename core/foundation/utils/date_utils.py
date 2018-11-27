from datetime import datetime, timedelta

import datetime as dt

Y_M_D_H_M_S = '%Y-%m-%d %H:%M:%S'
Y_M_D_H_M = '%Y-%m-%d %H:%M:00'
Y_M_D = '%Y-%m-%d'
fmt = '%Y-%m-%d %H:%M:%S.%f'


def current(format):
    return datetime.now().strftime(format)


def gmt8_bittrex(timestamp):
    return (datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f") + timedelta(hours=8)).strftime(fmt)


def gmt8_hitbtc(timestamp):
    return (datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=8)).strftime(fmt)


def utc_2_gmt(timestamp):
    if len(timestamp) == 10:
        return (datetime.fromtimestamp(int(timestamp))).strftime(fmt)
    else:
        return (datetime.fromtimestamp(int(timestamp) * 0.001)).strftime(fmt)


def add_date(date, format):
    return (dt.datetime.strptime(date, format) + dt.timedelta(days=1))


def to_string(date, format):
    return date.strftime(format)


def utc_date(string):
    return datetime.strptime(string, Y_M_D_H_M_S) + dt.timedelta(hours=-8)


def to_date(string, format):
    return datetime.strptime(string, format)


def format_date(date):
    month_pairs = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
        '-': '-'
    }
    year = date[-4:]
    day = date[4:6]
    month = month_pairs[date[:3] if date != '-' else '-']

    return year + "-" + month + "-" + day
