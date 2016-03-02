#!/usr/bin/env python
# Will Spurgin
# Joe St. Angelo

import urllib
import requests
import re
import string
import lxml
import sys
import csv

from robotparser import RobotFileParser
from urlparse import urlparse
from bs4 import BeautifulSoup
from collections import deque

# "constants"
__ROBOTS_TXT__ = "/robots.txt" # relative address of robots.txt from host
__USER_AGENT__ = "*"           # user agent to check in robots.txt
__HTTP__       = "http"

class Parser(object):
	"""
	The parsing workhorse of the entire project.
	"""

	def __init__(self, **kwargs):
		super(Parser, self).__init__()
		self.document_list = []
		