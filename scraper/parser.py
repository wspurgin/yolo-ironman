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
import hashlib
import porter

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
		self.document_dict = {}
		self.p = PorterStemmer()


	def retrieveText(self, page_soup):
		"""
		Retrieves all the non-markup text from a webpage that
		has already been crawled.

		@page_soup: The soupified version of a webpage
		"""
		# Retrieve all the text of the page minus the html tags
		page_text = page_soup.get_text()
		# Stems and returns all the text
		page_text = self.p.stemText(page_text)
		# Create a hash to make sure there are no 100% duplicates in the pages
		# The hex digest will also be used as the document ID, since they will be
		# unique unless they are a duplicate
		page_hash = hashlib.md5().update(page_text).hexdigest()
		# If the page is not a duplicate
		if page_hash not in self.document_dict:
			self.document_dict[page_hash] = page_text

