#!/usr/local/bin/python
# Will Spurgin
# 4/23/2014
# yolo-ironman Ironman

import urllib
import requests
import re

class Ironman(object):
    """The Tony Stark of web crawler classes. Yolo."""
    def __init__(self, **kwargs):
        super(Ironman, self).__init__()
        if kwargs['target_url']:
            self.target_url = kwargs['target_url']
        else:
            self.target_url = None
        if kwargs['pattern']:
            self.pattern = kwargs['pattern']
        else:
            self.pattern = None

    def read_data(self):
        if not self.target_url:
            raise Exception("No url set for instance of Ironman")
        if not self.pattern:
            raise Exception("No pattern set for instance of Ironman")
        node = requests.get(self.target_url)
        matches = re.findall(self.pattern, node.content)
        return matches

if __name__=="__main__":
    # sample testing
    url = "http://www.fairlabor.org/affiliates/participating-companies"
    pattern = '<a href="/affiliate/(.*)">' #regex pattern to get parent names
    yolo = Ironman(target_url=url, pattern=pattern)
    parents = yolo.read_data()
    print set(parents)
