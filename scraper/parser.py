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

	def __init__(self, stop_words, **kwargs):
		"""
		The constructor for the Parser object.

		@stop_words could be one a list of stop words, or None
		"""
		super(Parser, self).__init__()
		# Checks if stop_words is a list
		if stop_words is not None:
			self.stop_words = []
			for word in stop_words:
				self.stop_words.append(word.lower())
		else:
			self.stop_words = None
		self.documents = {}
		self.p = PorterStemmer()

	def retrieveText(self, page_soup):
		"""
		Retrieves all the non-markup text from a webpage that
		has already been crawled.

		@page_soup: The soupified version of a webpage
		"""
		# Retrieve all the text of the page minus the html tags
		page_text = page_soup.get_text()
		# Stems and returns all the non-stopword text
		page_text = self.p.stemText(page_text, self.stop_words)
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