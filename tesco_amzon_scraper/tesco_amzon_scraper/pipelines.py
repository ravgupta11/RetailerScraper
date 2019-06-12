# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import os

from scrapy import Request
from scrapy import signals
from scrapy.exporters import CsvItemExporter
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.xlib.pydispatch import dispatcher


class TescoAmzonScraperPipeline1(ImagesPipeline):
    def get_media_requests(self, item, info):
        return [Request(x, meta={'title': item['title'], 'breadcrumbs': item['breadcrumbs']}) for x in
                item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        ## end of deprecation warning block
        title = request.meta['title']
        _path = request.meta['breadcrumbs']
        return '%s/%s/IMG.jpg' % (_path, title)

class TescoAmzonScraperPipeline2(object):

    def __init__(self):
        dispatcher.connect(self.close_spider, signals.spider_closed)

    def cleanPrice(self, item, spider):
        if type(item['price']) == list:
            item['price'] = item['price'][0]

    def cleanTitle(self, item, spider):
        if type(item['title']) == list:
            item['title'] = item['title'][0]

        if spider.site == 'amazon':
            item['title'] = item['title'].replace(':', ' ').replace(',', '').replace('Amazon.com', '').strip()

    def cleanProduct(self, item, spider):
        if type(item['product_desc']) == list:
            item['product_desc'] = item['product_desc'][0]

    def cleanBreadcrumbs(self, item, spider):
        item['breadcrumbs'] = [x.strip(' \n') for x in item['breadcrumbs']]
        item['breadcrumbs'] = '/'.join(item['breadcrumbs'])

    def open_spider(self, spider):
        self.title_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.title_to_exporter.values():
            exporter.finish_exporting()
            exporter.file.close()


    def _exporter_for_item(self, item, spider):
        self.cleanTitle(item, spider)
        title = item['title']
        _path = ""
        try:
            _path = item['breadcrumbs']
        except:
            pass

        if (title, _path) not in self.title_to_exporter:
            PATH = 'FILES/' + _path + '/' + title
            if not os.path.exists(PATH):
                os.makedirs(PATH)
            if (spider.output == 'json'):
                f = open('%s/JS.json' % (PATH), 'wb')
                exporter = JsonItemExporter(f)
            else:
                f = open('%s/CSV.csv' % (PATH), 'wb')
                exporter = CsvItemExporter(f)
            exporter.start_exporting()
            self.title_to_exporter[(title, _path)] = exporter
        return self.title_to_exporter[(title, _path)]



    def process_item(self, item, spider):
        try:
            self.cleanBreadcrumbs(item, spider)
            self.cleanTitle(item, spider)
            self.cleanPrice(item, spider)
            self.cleanProduct(item, spider)
        except KeyError:
            pass
        exporter = self._exporter_for_item(item, spider)
        exporter.export_item(item)
        return item
