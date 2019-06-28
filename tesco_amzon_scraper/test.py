import unittest, os
from scrapy.http import TextResponse, Request
from tesco_amzon_scraper.utilities import applyResponse, to_str

def fake_response_from_file(file_name, url):

    request = Request(url=url)

    if not file_name[0] == '/':
        responses_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(responses_dir, file_name)
    else:
        file_path = file_name

    f = open(file_path, 'r', encoding='utf-8')
    file_content = f.read()
    f.close()

    response = TextResponse(url=url,
        request=request,
        body=file_content,
        encoding='utf-8')
    return response


class SpiderTest(unittest.TestCase):

    def test_check_price_passed1(self):
        self.resp = fake_response_from_file('html_sample.html', 'https://www.amazon.com/Samsung-500GB-Internal-MZ-76E500B-AM/dp/B0781Z7Y3S/ref=lp_16225007011_1_5?s=computers-intl-ship&ie=UTF8&qid=1561364439&sr=1-5')
        data = applyResponse(self.resp, '//div[@id="buybox"] //*[contains(@class, "color-price")]/text()').extract_first()
        self.assertEqual(data, '$77.99')

    def test_check_price_passed2(self):
        self.resp = fake_response_from_file('html_sample1.html', 'https://www.amazon.com/Wacom-Intuos-Small-Touch-Version/dp/B010LHRFYU')
        data = applyResponse(self.resp, '//div[@id="buybox"] //*[contains(@class, "color-price")]/text()').extract_first()
        self.assertEqual(data, '$43.72')

    def test_check_price_failed(self):
        self.resp = fake_response_from_file('html_sample2.html', 'https://docs.scrapy.org/en/latest/topics/downloader-middleware.html')
        data = applyResponse(self.resp, '//div[@id="buybox"] //*[contains(@class, "color-price")]/text()').extract_first()
        self.assertIsNone(data)

    def test_tostr1(self):
        item = ['value']
        item = to_str(item)
        self.assertEqual(item, 'value')

    def test_tostr2(self):
        item = 'value'
        item = to_str(item)
        self.assertEqual(item, 'value')

    def test_tostr3(self):
        item = [4]
        item = to_str(item)
        self.assertNotEqual(item, '4')
