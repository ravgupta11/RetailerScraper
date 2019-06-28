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
    AMAZON = '//div[@id="buybox"] //*[contains(@class, "color-price")]/text()'
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