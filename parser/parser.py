import requests
from xml.etree import ElementTree


class Parser(object):

    def __init__(self):
        self.url = 'http://revistaautoesporte.globo.com/rss/ultimas/feed.xml'
        self.xml_root = ''
        self.json = {'feed': []}

    def populate_xml_content(self):
        response = requests.get(self.url)
        self.xml_root = ElementTree.fromstring(response.content)

    def return_items_elements(self):
        return self.xml_root.findall('./channel/item')

    def parse_string_element(self, item, item_name):
        return item.find(item_name).text

    def parse_description_element(self, item):
        description = []

        desc_content = self.parse_string_element(item, 'description')

        return description

    def parse_item(self, item):
        item = {
            'title': self.parse_string_element(item, 'title'),
            'link': self.parse_string_element(item, 'link'),
            'description': self.parse_description_element(item)
        }
        return item

    def parse_xml(self):
        self.populate_xml_content()

        items = self.return_items_elements()

        for item in items:
            self.json['feed'].append(self.parse_item(item))

