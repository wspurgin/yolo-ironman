#!/usr/local/bin/python
# Will Spurgin
# 4/23/2014
# yolo-ironman Ironman

import urllib
import requests
import re

from robotparser import RobotFileParser
from urlparse import urlparse

class Ironman(object):
    """
    The Tony Stark of web crawler classes. Yolo.
    @param starting_url
    @param treat_as_host = false
    @kwargs
        pattern = regex pattern used to detect new URLS, compiled with `re` and
            with ignore case.
        bind_to_starting_host = boolean

    The `treat_as_host` option is useful if the starting URL is not actually a
    host such as http://lyle.smu.edu/~wspurgin
    """
    def __init__(self, starting_url, treat_as_host=False, **kwargs):
        super(Ironman, self).__init__()
        self.starting_url = starting_url
        self.treat_as_host = treat_as_host
        if self.treat_as_host:
            self.host = self.starting_url
        else:
            self.host = urlparse(self.starting_url).netloc
        self.pattern = re.compile('<a\s?.*href="(.+\w+)"\s*>', re.IGNORECASE)
        if 'pattern' in kwargs:
            self.pattern = re.compile(kwargs['pattern'], re.IGNORECASE)

        # Get Robots.txt and parse it for information.

    def crawl(self):
        if not self.starting_url:
            raise Exception("No url set for instance of Ironman")
        node = requests.get(self.starting_url)
        matches = re.findall(self.pattern, node.content)
        return matches

if __name__=="__main__":
    # sample testing
    starting_url = "http://lyle.smu.edu/~fmoore"
    yolo = Ironman(starting_url, treat_as_host=True)
    nodes = yolo.crawl()
    print set(nodes)
