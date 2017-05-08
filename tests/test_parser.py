import pytest
import os
import json
from mock import Mock
from xml.etree import ElementTree
from bs4 import BeautifulSoup

from parser.parser import Parser
from tests import test_scenarios


class TestParser():

    def setup_method(self):
        self.parser = Parser()

    def test_init(self):
        assert self.parser.url is not None
        assert self.parser.json is not None
        assert self.parser.json['feed'] is not None

    def test_populate_xml_content(self):
        self.parser.populate_xml_content()
        assert len(self.parser.xml_root) > 0

    @pytest.mark.parametrize('mock_xml, items_number',
                             test_scenarios.test_scenarios_items_elements)
    def test_return_items_elements(self, mock_xml, items_number):
        self.parser.xml_root = ElementTree.fromstring(mock_xml)

        res = self.parser.return_items_elements()
        assert len(res) == items_number

    def test_parse_string_element(self):
        mock_xml = ('<rss><channel> '
                    '   <item><tag_name>Content of tag</tag_name></item> '
                    '</channel></rss>')
        self.parser.xml_root = ElementTree.fromstring(mock_xml)

        items = self.parser.return_items_elements()
        res = self.parser.parse_string_element(items[0], 'tag_name')
        assert res == 'Content of tag'

    def test_parse_description_element(self):
        mock_xml = ('<rss><channel> '
                    '   <item>'
                    '       <description></description>'
                    '   </item> '
                    '</channel></rss>')
        self.parser.xml_root = ElementTree.fromstring(mock_xml)

        items = self.parser.return_items_elements()
        res = self.parser.parse_description_element(items[0])
        assert res == []

    def test_process_p_tag(self):
        description_list = []

        tag = ElementTree.Element('p')
        p_content = 'P Content'
        tag.text = p_content
        self.parser.process_p_tag(tag, description_list)

        assert description_list == [{'type': 'text', 'content': p_content}]

    def test_process_p_tag_without_value(self):
        description_list = []

        tag = ElementTree.Element('p')
        tag.text = '  '
        self.parser.process_p_tag(tag, description_list)

        assert description_list == []

    def test_process_div_img_tag(self):
        description_list = []

        soup = BeautifulSoup('<img src=\'img_src\'></img>', "html.parser")
        self.parser.process_div_img_tag(soup.find('img'), description_list)

        assert description_list == [{'type': 'image', 'content': 'img_src'}]

    def test_process_div_ul_tag(self):
        description_list = []

        soup = BeautifulSoup('<ul> '
                             '  <li><a href=\'link1\'/></li> '
                             '  <li><a href=\'link2\'/></li>'
                             '<ul>', "html.parser")

        self.parser.process_div_ul_tag(soup.find('ul'), description_list)

        assert description_list == [
            {'type': 'links',
             'content': ['link1', 'link2']}
        ]

    def test_process_div_tag(self):
        description_list = []

        soup = BeautifulSoup('<div>'
                             '<img src=\'img_src\'/>'
                             '<ul> '
                             '  <li><a href=\'link1\'/></li> '
                             '  <li><a href=\'link2\'/></li>'
                             '</ul>'
                             '</div>', "html.parser")

        self.parser.process_div_tag(soup.find('div'), description_list)

        assert description_list == [
            {'type': 'image', 'content': 'img_src'},
            {'type': 'links', 'content': ['link1', 'link2']},
        ]

    def test_parse_item(self):
        mock_xml = ('<rss><channel> <item>'
                    '   <title>Title</title>'
                    '   <link>URL Link</link>'
                    '   <description>Content of description</description>'
                    '</item> </channel></rss>')
        self.parser.xml_root = ElementTree.fromstring(mock_xml)

        items = self.parser.return_items_elements()
        res = self.parser.parse_item(items[0])
        assert res['title'] == 'Title'
        assert res['link'] == 'URL Link'
        assert res['description'] == []

    def test_parse_xml(self):
        self.parser.populate_xml_content = Mock(
            side_effect=self.side_effect_file
        )
        self.parser.parse_xml()

        assert self.parser.json == test_scenarios.feed_input_file_expected_json

    def side_effect_file(*args, **kwargs):
        folder = os.path.dirname(__file__)
        file_path = os.path.join(folder, 'feed_input_test.xml')

        args[0].parser.xml_root = ElementTree.parse(file_path).getroot()
