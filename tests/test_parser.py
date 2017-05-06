import unittest
import requests
from parser.parser import Parser


class TestParser(unittest.TestCase):

    def test_get_feed_url_content(self):
        parser = Parser()
        response = parser.get_feed_url_content()
        self.assertEqual(response.status_code, requests.codes.ok)
        self.assertEqual(response.headers.get('Content-Type'), 'text/xml; charset=utf-8')

if __name__ == '__main__':
    unittest.main()
