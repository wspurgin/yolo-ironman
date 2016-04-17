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

	def __init__(self, full_text, stem_text, url, hash_id):
		super(Document, self).__init__()
		self.url = url
		self.full_text = full_text
		self.stem_text = stem_text
		self.id = hash_id
		text_list = stem_text.split()
		self.word_vector = {x:text_list.count(x) for x in text_list}
