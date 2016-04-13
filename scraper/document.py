#!/usr/bin/env python
# Will Spurgin
# Joe St. Angelo
# yolo-ironman Ironman

import urllib
import requests
import re
import string
import hashlib
import lxml
import sys
import time

class Document(object):
	"""
	The document object that will keep track of all the relevant info
	for each document that the crawler comes across. Used especially
	specifically to make indexing and searching an easier and quicker
	process.
	"""

	def __init__(self, url, text):
		super(Document, self).__init__()
		self.url = url
		self.text = text.split(' ')[:20]
		h = hashlib.md5()
		h.update(text)
		self.hash = h.hexdigest()
