from enum import Enum

class SITE_DOMAIN(Enum):
    AMAZON = 'www.amazon.com'
    TESCO = 'www.tesco.com'
    ASDA = 'groceries.asda.com'

class SITE_URL(Enum):
    AMAZON = 'https://www.amazon.com/'
    TESCO =  'https://www.tesco.com/groceries/en-GB/shop'
    ASDA = 'https://groceries.asda.com/'

class SITE_RULE(Enum):
    AMAZON = r"(?:\/dp\/)|(?:\/gp\/product\/)"
    TESCO = r"(?:\/products\/)"
    ASDA = r"(?:groceries.asda.com\/product\/)"

class PRICE(Enum):
    AMAZON = '//*[@id="priceblock_ourprice"]/text()'
    TESCO = '//div[@class="product-details-tile"]//span[@class="value"]/text()'
    ASDA = '//div[@class="pd-right-cont"]//p[@class="prod-price"]/span[@class="prod-price-inner"]/text()'

class TITLE(Enum):
    AMAZON = '//head/title/text()'
    TESCO = '//h1[@class="product-details-tile__title"]/text()'
    ASDA = '//div[@class="pd-right-cont"]//h1[@class="prod-title"]/text()'

class IMAGE(Enum):
    AMAZON = '//div[@id="leftCol"]//div[@id="main-image-container"]//img/@data-old-hires'
    TESCO = '//div[@class="product-details-tile__main"]//img/@src'
    ASDA = '//div[@class="pd-left-cont"]//div[@class="pld-img-container"]//img/@src'

class BREADCRUMBS(Enum):
    AMAZON = '//ul[@class="a-unordered-list a-horizontal a-size-small"]/li/span/a/text()'
    TESCO = '//ol/li/div/span/a/span/span/text()'
    ASDA = '//div[@id = "newBreadcrumb"]/ul/li/a/text()'

class DESC(Enum):
    AMAZON = '//meta[contains(@name, "description")]/@content'
    TESCO = '//head/meta[@name="description"]/@content'
    ASDA = '//head/meta[@name ="description"]/@content'

def applyResponse(response, expression):
    return response.xpath(expression)

class AmazonTescoDetails:
    def getImg(self, response, retailer_image):
        return applyResponse(response, retailer_image).get()
    def getCrumbs(self, response, retailer_breadcrum):
        return applyResponse(response, retailer_breadcrum).extract()

class AmazonDetails(AmazonTescoDetails):

    def getPrice(self, response):
        return applyResponse(response, PRICE.AMAZON.value).get()

    def getImg(self, response):
        return AmazonTescoDetails().getImg(response, IMAGE.AMAZON.value)

    def getCrumbs(self, response):
        return AmazonTescoDetails().getCrumbs(response, BREADCRUMBS.AMAZON.value)

    def getProduct(self, response):
        return applyResponse(response, DESC.AMAZON.value).get()

    def getTitle(self, response):
        return applyResponse(response, TITLE.AMAZON.value).get()

    def getURL(self):
        return SITE_URL.AMAZON.value

    def getDomain(self):
        return SITE_DOMAIN.AMAZON.value

    def getRule(self):
        return SITE_RULE.AMAZON.value

class Tesco:

    def getPrice(self, response):
        return applyResponse(response, PRICE.TESCO.value).extract_first()

    def getImg(self, response):
        return applyResponse(response, IMAGE.TESCO.value).get()

    def getCrumbs(self, response):
        return applyResponse(response, BREADCRUMBS.TESCO.value).extract()

    def getProduct(self, response):
        return applyResponse(response, DESC.TESCO.value).get()

    def getTitle(self, response):
        return applyResponse(response, TITLE.TESCO.value).get()

    def getURL(self):
        return SITE_URL.TESCO.value

    def getDomain(self):
        return SITE_DOMAIN.TESCO.value

    def getRule(self):
        return SITE_RULE.TESCO.value

class Asda:

    def getPrice(self, response):
        return applyResponse(response, PRICE.ASDA.value).get()

    def getImg(self, response):
        return applyResponse(response, IMAGE.ASDA.value).get()

    def getCrumbs(self, response):
        return applyResponse(response, BREADCRUMBS.ASDA.value).extract()

    def getProduct(self, response):
        return applyResponse(response, DESC.ASDA.value).get()

    def getTitle(self, response):
        return applyResponse(response, TITLE.ASDA.value).get()

    def getURL(self):
        return SITE_URL.ASDA.value

    def getDomain(self):
        return SITE_DOMAIN.ASDA.value

    def getRule(self):
        return SITE_RULE.ASDA.value
