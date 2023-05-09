# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SrcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    src=scrapy.Field()
    src_abbr=scrapy.Field()
    url=scrapy.Field()
    classes=scrapy.Field()
    level=scrapy.Field()
    types=scrapy.Field()
    publisher=scrapy.Field()
