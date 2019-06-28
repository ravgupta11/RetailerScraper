# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from tesco_amzon_scraper.RetailersDetails import AmazonDetails, TescoDetails, AsdaDetails
from tesco_amzon_scraper.items import TescoAmzonScraperItem


def makeObject(spider):
    if spider.site == 'amazon':
        return AmazonDetails()
    elif spider.site == 'tesco':
        return TescoDetails()
    elif spider.site == 'asda':
        return AsdaDetails()
    else:
        print("Site name is invalid.")
        exit(0)


class RetailerSpider(CrawlSpider):
    name = 'retailerSpider'

    def parse_items(self, response):
        item = ItemLoader(item=TescoAmzonScraperItem(), response=response)
        item.add_value('title', self.o.getTitle(response))
        item.add_value('price', self.o.getPrice(response))
        item.add_value('image_urls', self.o.getImg(response))
        item.add_value('product_desc', self.o.getProduct(response))
        item.add_value('breadcrumbs', self.o.getCrumbs(response))
        return item.load_item()

    def __init__(self, output='', site='', *args, **kwargs):
        self.output = output
        self.site = site
        self.o = makeObject(self.site)
        self.allowed_domains = [self.o.getDomain()]
        self.start_urls = [self.o.getURL()]
        self.rules = [
            Rule(LinkExtractor(allow=self.o.getRule()), callback='parse_items', follow=True),
            Rule(LinkExtractor(unique=True, canonicalize=True)), ]

        super(RetailerSpider, self).__init__(*args, **kwargs)
