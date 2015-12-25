# -*- coding: utf-8 -*-
import scrapy


# Define the models for scraped items
class SpiderItem(scrapy.Item):
    ID = scrapy.Field()
    URL = scrapy.Field()
    Time = scrapy.Field()
    Keyword = scrapy.Field()
    Source = scrapy.Field()
    Channel = scrapy.Field()

    Total = scrapy.Field()

    Title = scrapy.Field()
    Artical = scrapy.Field()
    Comment = scrapy.Field()
    Html = scrapy.Field()

