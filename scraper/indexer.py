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

class Indexer(object):
	"""
	The indexer of this entire operation. This object can
	manipulate a dictionary of Document IDs and the full text of documents
	to create an inverse document frequency index.
	"""

	def __init__(self, **kwargs):
		super(Indexer, self).__init__()
		self.word_index = {}

	def indexWords(self, document_dic):
		"""
		Reads each word in the dociment_dic and creates an inverse doc list
		with also its frequency in that document. The inverse doc is a dictionary
		that relates each word to a list that contains tuples of the docID, and the 
		frequency of that word in that doc.
		E.g.
		the => [(doc1, 4), (doc2, 3), (doc3, 6)]
		banana => [(doc1, 1), (doc3, 1)]
		"""
		# Goes through all the documents in the dictionary
		for key in document_dic:
			# Grabs each document's text
			doc_text = document_dic[key]
			# Splits the text up into individual words in a list
			word_list = doc_text.split()
			# Goes through each word
			for word in word_list:
				# Checks to see if the word has been indexed yet
				if word in self.word_index:
					# Tests for if this docID has been already related
					# to this specific word
					found_doc = False
					# Grabs the index and tuple of the index for the
					# specific word
					for idx, doc in enumerate(self.word_index[word]):
						# If one of the doc IDs matches the current
						# doc ID, then increment the frequency of that
						# word by 1
						if doc[0] == key:
							# Going from left to right:
							# 1. Grab the appropriate list of tuples from
							#	 the index based on the word
							# 2. Go to the appropriate index of the tuple
							#	 that matches the docID
							# 3. Grab the frequency value
							# 4. Increment by 1
							self.word_index[word][idx][1] += 1
							found_doc = True
							break
					# If this is the first occurenec of this word in this
					# document
					if not found_word:
						# Add the tuple to this list
						self.word_index[word].append((key, 1))						
				else:
					# Adds the word to the index, and relates to
					# a list of tuples that contain the docID and
					# the number of occurences of that word
					self.word_index[word] = [(key, 1)]

	def findMostFreq(self, top_x=20):
		"""
		Finds the most frequent words in the entire collection,
		and returns a certain amount.

		@top_x: The top x number of results to return. By default, it
		returns the top 20 most frequent results
		"""
		#TODO: This
		print "Howdy!"

if __name__ == "__main__":
