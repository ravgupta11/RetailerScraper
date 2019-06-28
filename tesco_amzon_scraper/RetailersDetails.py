from interface import Interface, implements
from tesco_amzon_scraper.constants import SITE_RULE, SITE_URL, SITE_DOMAIN, DESC, PRICE, TITLE, IMAGE, BREADCRUMBS
from tesco_amzon_scraper.utilities import applyResponse

class Details(Interface):
    def getPrice(self, response):
        pass

    def getImg(self, response):
        pass

    def getCrumbs(self, response):
        pass

    def getProduct(self, response):
        pass

    def getTitle(self, response):
        pass

    def getURL(self):
        pass

    def getDomain(self):
        pass

    def getRule(self):
        pass





class AmazonTescoDetails:
    def getImg(self, response, retailer_image):
        return applyResponse(response, retailer_image).get()

    def getCrumbs(self, response, retailer_breadcrum):
        return applyResponse(response, retailer_breadcrum).extract()


class AmazonDetails(AmazonTescoDetails, implements(Details)):

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


class TescoDetails(implements(Details)):

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


class AsdaDetails(implements(Details)):

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
