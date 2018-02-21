# -*- coding:utf-8 -*-
import scrapy

class LlssAllItem(scrapy.Item):
    title = scrapy.Field()
    post_date = scrapy.Field()
    abstract = scrapy.Field()
    magnet = scrapy.Field()
    image_urls = scrapy.Field()
    image_type = scrapy.Field()
