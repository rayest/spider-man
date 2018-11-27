import random

from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

from core.settings import IP_POOL, USER_AGENT_POOL


class HttpProxy(HttpProxyMiddleware):

    def __init__(self, ip=''):
        super().__init__()
        self.ip = ip

    def process_request(self, request, spider):
        ip_port = random.choice(IP_POOL)
        request.meta['proxy'] = 'https://' + ip_port['ip_port']


class UserAgent(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        super().__init__(user_agent)
        self.user_agent = user_agent

    def process_request(self, request, spider):
        this_user_agent = random.choice(USER_AGENT_POOL)
        request.headers.setdefault('User-Agent', this_user_agent)
        request.headers.setdefault('Connection', 'keep-alive')
