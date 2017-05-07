import requests
from xml.etree import ElementTree
from collections import OrderedDict


class Parser(object):

    def __init__(self):
        self.url = 'http://revistaautoesporte.globo.com/rss/ultimas/feed.xml'
        self.xml_root = ''
        self.json = OrderedDict({'feed': []})

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
        description_list.append({'type': 'image', 'content': tag.attrib['src']})

    def process_div_ul_tag(self, tag, description_list):
        content_list = []
        for li_tag in tag.iter():
            tag_name = li_tag.tag
            if tag_name == 'li':
                content_list.append(li_tag.text)

        description_list.append({'type': 'links', 'content': content_list})

    def process_div_tag(self, tag, description_list):
        for children_tag in tag.iter():
            tag_name = children_tag.tag

            if tag_name == 'img':
                self.process_div_img_tag(children_tag, description_list)

            if tag_name == 'ul':
                self.process_div_ul_tag(children_tag, description_list)

    def parse_description_element(self, item):

        description_list = []

        p_child = item.find('description').findall('p')

        for children_tag in p_child:
            self.process_p_tag(children_tag, description_list)

        div_child = item.find('description').findall('div')

        for children_tag in div_child:
            self.process_div_tag(children_tag, description_list)

        return description_list

    def parse_item(self, item):
        item = OrderedDict({
            'title': self.parse_string_element(item, 'title'),
            'link': self.parse_string_element(item, 'link'),
            'description': self.parse_description_element(item)
        })
        return item

    def parse_xml(self):
        self.populate_xml_content()

        items = self.return_items_elements()

        for item in items:
            self.json['feed'].append(self.parse_item(item))
