import scrapy


class StartplayingItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    cost = scrapy.Field()
    image = scrapy.Field()
    seats_left = scrapy.Field()
    game_system = scrapy.Field()
    tactical_level = scrapy.Field()
