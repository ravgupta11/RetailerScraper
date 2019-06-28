# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from tesco_amzon_scraper.items import TescoAmzonScraperItem


class Sp2Spider(CrawlSpider):
    name = 'sp2'
    allowed_domains = ['www.tesco.com']
    start_urls = ['https://www.tesco.com/groceries/en-GB/shop']
    rules = [
        Rule(LinkExtractor(allow=r"(?:\/products\/)"), callback='parse_items', follow=True),
        Rule(LinkExtractor(unique=True, canonicalize=True)),
    ]

    def getPrice(self, response):
        if self.site == 'amazon':
            return response.xpath('//*[@id="priceblock_ourprice"]/text()').get()
        if self.site == 'tesco':
            return response.xpath(
                '//div[@class="product-details-tile"]//span[@class="value"]/text()').extract_first()
        if self.site == "asda":
            return response.xpath(
                '//div[@class="pd-right-cont"]//p[@class="prod-price"]/span[@class="prod-price-inner"]/text()').get()

    def getImg(self, response):
        if self.site == 'amazon':
            return response.xpath('//*[@id="landingImage"]/@data-old-hires').get()
        if self.site == 'tesco':
            return response.xpath('//div[@class="product-details-tile__main"]//img/@src').get()
        if self.site == 'asda':
            return response.xpath('//div[@class="pd-left-cont"]//div[@class="pld-img-container"]//img/@src').get()

    def getBreadcrumbs(self, response):
        if self.site == 'amazon':
            return response.xpath(
                '//ul[@class="a-unordered-list a-horizontal a-size-small"]/li/span/a/text()').extract()
        if self.site == 'tesco':
            return response.xpath('//ol/li/div/span/a/span/span/text()').extract()
        if self.site == 'asda':
            return response.xpath('//div[@id = "newBreadcrumb"]/ul/li/a/text()').extract()

    def getTitle(self, response):
        if self.site == 'amazon':
            return response.xpath('//head/title/text()').get()
        if self.site == 'tesco':
            return response.xpath('//h1[@class="product-details-tile__title"]/text()').get()
        if self.site == 'asda':
            return response.xpath('//div[@class="pd-right-cont"]//h1[@class="prod-title"]/text()').get()

    def getProduct(self, response):
        if self.site == 'amazon':
            return response.xpath('//meta[contains(@name, "description")]/@content').get()
        if self.site == 'tesco':
            return response.xpath('//head/meta[@name="description"]/@content').get()
        if self.site == 'asda':
            return response.xpath('//head/meta[@name ="description"]/@content').get()

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
        super(Sp2Spider, self).__init__(*args, **kwargs)
