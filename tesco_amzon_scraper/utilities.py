
def applyResponse(response, expression):
    return response.xpath(expression)


def to_str(item):
    if type(item) == list:
        return item[0]
    else:
        return item

def cleanTitle(item):
    if type(item) == list:
        item = item[0]
        item = item.replace(':', ' ').replace(',', '').replace('Amazon.com', '').strip()
        return item
    else:
        return item


def cleanBreadcrumbs(item):
    item = [x.strip(' \n') for x in item]
    item = '/'.join(item)
    return item
