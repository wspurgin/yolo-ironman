#!/usr/bin/env python
# Will Spurgin
# Joe St. Angelo

import requests
import string
import lxml
import sys
import hashlib

from porter import PorterStemmer
from bs4 import BeautifulSoup

class Parser(object):
	"""
	The parsing workhorse of the entire project.
	"""

	def __init__(self, **kwargs):
		super(Parser, self).__init__()
		self.documents = {}
		self.p = PorterStemmer()

	def retrieveText(self, page_soup):
		"""
		Retrieves all the non-markup text from a webpage that
		has already been crawled.

		@page_soup: The soupified version of a webpage
		"""
		# Retrieve all the text of the page minus the html tags
		page_text = str(page_soup.get_text())
		# Stems and returns all the text
		page_text = self.p.stemText(page_text)
		# Create a hash to make sure there are no 100% duplicates in the pages
		# The hex digest will also be used as the document ID, since they will
		# be unique unless they are a duplicate
		h = hashlib.md5()
		h.update(page_text)
		page_hash = h.hexdigest()
		# If the page is not a duplicate
		if page_hash not in self.documents:
			self.documents[page_hash] = page_text

if __name__ == "__main__":
	test_url = "http://lyle.smu.edu/~jstangelo/IR/test.html"
	req = requests.get(test_url)
	page_soup = BeautifulSoup(req.content, "lxml")
	p = Parser()
	p.retrieveText(page_soup)
	print p.documents