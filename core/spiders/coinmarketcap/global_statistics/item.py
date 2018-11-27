import scrapy


class GlobalItem(scrapy.Item):
    active_cryptocurrencies = scrapy.Field()
    active_markets = scrapy.Field()
    bitcoin_percentage_of_market_cap = scrapy.Field()
    total_market_cap_by_available_supply_usd = scrapy.Field()
    total_volume_usd = scrapy.Field()
