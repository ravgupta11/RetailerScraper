import os
from scrapy import Request
from scrapy.exporters import CsvItemExporter
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from tesco_amzon_scraper.utilities import cleanTitle, to_str, cleanBreadcrumbs

class TescoAmzonScraperPipeline1(ImagesPipeline):

    def get_media_requests(self, item, info):
        return [Request(x, meta={'title': item['title'], 'breadcrumbs': item['breadcrumbs']}) for x in
                item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):

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
        # end of deprecation warning block
        _title = request.meta['title']
        _path = request.meta['breadcrumbs']
        return '%s\%s\IMG.jpg' % (_path, _title)


class TescoAmzonScraperPipeline2(object):


    def open_spider(self, spider):
        self.title_to_exporter = {}

    def close_spider(self, spider):
        for exporter in self.title_to_exporter.values():
            exporter.finish_exporting()
            exporter.file.close()


    def _exporter_for_item(self, item, spider):
        _title = item['title']
        _path = ""
        try:
            _path = item['breadcrumbs']
        except:
            pass
        if (_title, _path) not in self.title_to_exporter:
            PATH = 'FILES\\' + _path + '\\' + _title
            if not os.path.exists(PATH):
                os.makedirs(PATH)
            if (spider.output == 'json'):
                f = open('%s\JS.json' % (PATH), 'wb')
                exporter = JsonItemExporter(f)
            else:
                f = open('%s\CSV.csv' % (PATH), 'wb')
                exporter = CsvItemExporter(f)
            exporter.start_exporting()
            self.title_to_exporter[(_title, _path)] = exporter
        return self.title_to_exporter[(_title, _path)]



    def process_item(self, item, spider):
        try:
            item['breadcrumbs'] = cleanBreadcrumbs(item['breadcrumbs'])
            item['title'] = cleanTitle(item['title'])
            item['price'] = to_str(item['price']).strip('\n').strip()
            item['product_desc'] = to_str(item['product_desc'])
        except KeyError:
            raise DropItem()
        exporter = self._exporter_for_item(item, spider)
        exporter.export_item(item)
        return item
