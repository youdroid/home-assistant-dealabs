import xml.etree.ElementTree as ET


class Deal:

    def __init__(self, category, merchant, price, title, description, link, pubDate):
        self.category = category
        self.merchant = merchant
        self.price = price
        self.title = title
        self.description = description
        self.link = link
        self.pubDate = pubDate

    @staticmethod
    def getAll(data):
        tree = ET.fromstring(data)
        deals = []
        for child in tree.findall('./channel/item'):
            d = Deal(child.find('category').text, child.find('{http://www.pepper.com/rss}merchant').attrib.get('name'),
                     child.find('{http://www.pepper.com/rss}merchant').attrib.get('price'), child.find('title').text,
                     child.find('description').text, child.find('link').text, child.find('pubDate').text)
            deals.append(d)
        return deals
