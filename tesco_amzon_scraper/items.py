# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TescoAmzonScraperItem(scrapy.Item):
    title = scrapy.Field()
    price = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    breadcrumbs = scrapy.Field()
    product_desc = scrapy.Field()
