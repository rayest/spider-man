class Spider(object):
    name = market = spider_start_time = reference_no = None

    def build_from(self, exchange_name, name, start_time, reference_no):
        self.reference_no = reference_no
        self.spider_start_time = start_time
        self.market = exchange_name
        self.name = name
        return self
