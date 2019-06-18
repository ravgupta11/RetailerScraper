# -*- coding: utf-8 -*-
from tesco_amzon_scraper.items import TescoAmzonScraperItem
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from tesco_amzon_scraper.getters import Amazon, Tesco, Asda, XYZ

def makeObject(spider):
    if spider.site == 'amazon':
        return Amazon()
    elif spider.site == 'tesco':
        return Tesco()
    elif spider.site == 'asda':
        return Asda()
    else:
        print("Site name is invalid.")
        exit(0)

class AmazonSpider(CrawlSpider):
    name = 'amazon'

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
        self.o = Amazon()
        self.allowed_domains = [self.o.getDomain()]
        self.start_urls = [self.o.getURL()]
        self.rules = [
            Rule(LinkExtractor(allow= self.o.getRule()), callback='parse_items', follow=True),
            Rule(LinkExtractor(unique=True, canonicalize=True)),]

        super(Sp1Spider, self).__init__(*args, **kwargs)