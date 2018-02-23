# -*- coding:utf-8 -*-
import scrapy

class LlssAllItem(scrapy.Item):
    title = scrapy.Field()
    post_date = scrapy.Field()
    abstract = scrapy.Field()
    magnet_with_prefix = scrapy.Field()
    magnet_without_prefix = scrapy.Field()
    image_urls = scrapy.Field()
    image_type = scrapy.Field()
