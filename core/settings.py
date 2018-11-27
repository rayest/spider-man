# -*- coding: utf-8 -*-

BOT_NAME = 'core'

SPIDER_MODULES = ['core.spiders']
NEWSPIDER_MODULE = 'core.spiders'

ROBOTSTXT_OBEY = True
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.1
AUTOTHROTTLE_MAX_DELAY = 0.5
LOG_ENABLED = False
# LOG_LEVEL = 'INFO'

IP_POOL = [
    {'ip_port': '45.77.95.158:8123'},
    {'ip_port': '66.82.144.29:8080'},
    {'ip_port': '167.99.12.78:3128'},
    {'ip_port': '208.167.242.216:8080'},
    {'ip_port': '66.82.123.234:8080'}
]

USER_AGENT_POOL = [
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36(KHTML, likeGecko) Chrome/65.0.3325.181 Mobile Safari/537.36',
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1"

]

COOKIES_ENABLED = False
