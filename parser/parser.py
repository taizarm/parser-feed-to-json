import requests
import json
from xml.etree import ElementTree

from bs4 import BeautifulSoup


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

    def process_p_tag(self, tag, description_list):
        p_content = tag.text.strip()
        if p_content:
            description_list.append({'type': 'text', 'content': p_content})

    def process_div_img_tag(self, tag, description_list):
        description_list.append({'type': 'image', 'content': tag['src']})

    def process_div_ul_tag(self, tag, description_list):
        content_list = []
        for li_tag in tag.find_all('li'):
            content_list.append(li_tag.find('a')['href'])

        description_list.append({'type': 'links', 'content': content_list})

    def process_div_tag(self, tag, description_list):
        for children_tag in tag.find_all():
            if children_tag.name == 'img':
                self.process_div_img_tag(children_tag, description_list)

            if children_tag.name == 'ul':
                self.process_div_ul_tag(children_tag, description_list)

    def parse_description_element(self, item):
        description_list = []

        desc = item.find('description')

        try:
            soup = BeautifulSoup(desc.text, "html.parser")

            for children_tag in soup.find_all():
                if children_tag.name == 'p':
                    self.process_p_tag(children_tag, description_list)
                elif children_tag.name == 'div':
                    self.process_div_tag(children_tag, description_list)

        except TypeError:
            pass

        return description_list

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


if __name__ == '__main__':

    parser = Parser()
    parser.parse_xml()
    print(json.dumps(parser.json, sort_keys=True, indent=4,
                     separators=(',', ': ')))
