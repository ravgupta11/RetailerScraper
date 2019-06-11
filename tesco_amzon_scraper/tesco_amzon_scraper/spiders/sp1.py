# -*- coding: utf-8 -*-
from tesco_amzon_scraper.items import TescoAmzonScraperItem
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule


class Sp1Spider(CrawlSpider):
    name = 'sp1'
    allowed_domains = ['www.amazon.com']
    start_urls = ['https://www.amazon.com/']
    rules = [
        Rule(LinkExtractor(allow=r"(?:\/dp\/)|(?:\/gp\/product\/)"), callback='parse_items', follow=True),
        Rule(LinkExtractor(unique=True, canonicalize=True)),
    ]

    def getPrice(self, response):
        if self.site == 'amazon':
            return response.xpath('//*[@id="priceblock_ourprice"]/text()').get()
        if self.site == 'tesco':
            return response.xpath(
                '//div[@class="product-control-wrapper"]/span[@data-auto ="price-value"]/text()').get()

    def getImg(self, response):
        if self.site == 'amazon':
            return response.xpath('//*[@id="landingImage"]/@data-old-hires').get()
        if self.site == 'tesco':
            return response.xpath('////img[@class="product-image"]/@src').get()

    def getBreadcrumbs(self, response):
        if self.site == 'amazon':
            return response.xpath(
                '//ul[@class="a-unordered-list a-horizontal a-size-small"]/li/span/a/text()').extract()
        if self.site == 'tesco':
            return response.xpath('//ol/li/div/span/a/span/span/text()').extract()

    def getTitle(self, response):
        if self.site == 'amazon':
            return response.xpath('//head/title/text()').get()
        if self.site == 'tesco':
            return response.xpath('//h1[@class="product-details-tile__title"]/text()').get()

    def getProduct(self, response):
        if self.site == 'amazon':
            return response.xpath('//meta[contains(@name, "description")]/@content').get()
        if self.site == 'tesco':
            return response.xpath('//head/meta[@name="description"]/@content').get()

    def parse_items(self, response):
        item = ItemLoader(item=TescoAmzonScraperItem(), response=response)
        item.add_value('title', self.getTitle(response))
        item.add_value('price', self.getPrice(response))
        item.add_value('image_urls', self.getImg(response))
        item.add_value('product_desc', self.getProduct(response))
        item.add_value('breadcrumbs', self.getBreadcrumbs(response))
        return item.load_item()

    def __init__(self, output='', site='', *args, **kwargs):
        self.output = output
        self.site = site
        super(Sp1Spider, self).__init__(*args, **kwargs)