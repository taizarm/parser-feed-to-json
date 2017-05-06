import pytest
from xml.etree import ElementTree
from parser.parser import Parser


class TestParser():

    test_scenarios_items_elements = [
        ('<rss><channel></channel></rss>', 0),
        ('<rss><channel> <item></item> <item></item> </channel></rss>', 2)
    ]

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
                             test_scenarios_items_elements)
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
        mock_xml = ('<rss><channel> '
                    '   <item><tag_name>Content of tag</tag_name></item> '
                    '</channel></rss>')
        self.parser.xml_root = ElementTree.fromstring(mock_xml)

        self.parser.parse_xml()
        assert 'feed' in self.parser.json
