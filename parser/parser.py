import requests


class Parser(object):

    def __init__(self):
        self.url = 'http://revistaautoesporte.globo.com/rss/ultimas/feed.xml'

    def get_feed_url_content(self):
        return requests.get(self.url)
