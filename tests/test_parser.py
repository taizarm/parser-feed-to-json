import pytest
from xml.etree import ElementTree
from mock import Mock
from parser.parser import Parser
from tests.test_scenarios import test_scenarios_items_elements, test_scenarios_parser


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

        tag = ElementTree.Element('img')
        src_img = 'src_img'
        tag.attrib = {'src': src_img}
        self.parser.process_div_img_tag(tag, description_list)

        assert description_list == [{'type': 'image', 'content': src_img}]

    def test_process_div_ul_tag(self):
        description_list = []

        tag = ElementTree.Element('ul')

        sub_tag_1 = ElementTree.SubElement(tag, 'li')
        li1_text = 'First Content'
        sub_tag_1.text = li1_text

        sub_tag_2 = ElementTree.SubElement(tag, 'li')
        li2_text = 'Second Content'
        sub_tag_2.text = li2_text

        self.parser.process_div_ul_tag(tag, description_list)

        assert description_list == [{'type': 'links', 'content': [li1_text, li2_text]}]

    def test_process_div_tag(self):
        description_list = []

        tag = ElementTree.Element('div')

        sub_tag_1 = ElementTree.SubElement(tag, 'ul')
        sub_sub_tag_1 = ElementTree.SubElement(sub_tag_1, 'li')
        li1_text = 'First Content'
        sub_sub_tag_1.text = li1_text

        sub_tag_2 = ElementTree.SubElement(tag, 'img')
        src_img = 'src_img'
        sub_tag_2.attrib = {'src': src_img}

        sub_tag_3 = ElementTree.SubElement(tag, 'span')
        sub_tag_3.text = 'Loren Ipsum'

        self.parser.process_div_tag(tag, description_list)

        assert description_list == [{'type': 'links', 'content': [li1_text]},
                                    {'type': 'image', 'content': src_img}]

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

    @pytest.mark.parametrize('xml_content, expected_json',
                             test_scenarios_parser)
    def test_parse_xml(self, xml_content, expected_json):
        self.parser.xml_root = ElementTree.fromstring(xml_content)

        self.parser.populate_xml_content = Mock(
            side_effect=(self.side_effect(xml_content))
        )
        self.parser.parse_xml()

        assert self.parser.json == expected_json

    def side_effect(*args, **kwargs):
        args[0].parser.xml_root = ElementTree.fromstring(args[1])
