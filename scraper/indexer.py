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
		# Contains the index of word to documents/frequency
		self.word_index = {}
		# Keeps track of the total frequency. Keeps track of
		# number of total occurences, and the number of documents
		# it appears in.
		self.word_freq = {}
		self.word_sorted = []

	def indexWords(self, doc_dic):
		"""
		Reads each word in the dociment_dic and creates an inverse doc list
		with also its frequency in that document. The inverse doc is a 
		dictionary that relates each word to a list that contains tuples of the
		docID, and the frequency of that word in that doc.
		E.g.
		the => [(doc1, 4), (doc2, 3), (doc3, 6)]
		banana => [(doc1, 1), (doc3, 1)]
		"""
		# Goes through all the documents in the dictionary
		for key in doc_dic:
			# Grabs each document's text
			doc_text = doc_dic[key]
			# Splits the text up into individual words in a list
			word_list = doc_text.split()
			# Goes through each word
			for word in word_list:
				# Checks to see if the word has been indexed yet
				if word in self.word_index:
					# Tests for if this docID has been already related
					# to this specific word
					found_word = False
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
							# 2. Go to the appropriate index of the 2-list
							#	 that matches the docID
							# 3. Grab the frequency value
							# 4. Increment by 1
							self.word_index[word][idx][1] += 1
							self.word_freq[word][1] += 1
							found_word = True
							break
					# If this is the first occurence of this word in this
					# document
					if not found_word:
						# Add the 2-list to the index list
						self.word_index[word].append([key, 1])	
						# Start tracking the total frequency in the collection
						self.word_freq[word][0] += 1
						self.word_freq[word][1] += 1					
				else:
					# Adds the word to the index, and relates to
					# a 2-list that contain the docID and
					# the number of occurences of that word
					self.word_index[word] = [[key, 1]]
					# Adds the word to frequency tracker. First number
					# is the doc frequency, second is the collection frequency
					self.word_freq[word] = [1, 1]
		# Creates a list of tuples sorted by the total frequency of a 
		# word throughout the entire collection
		self.word_sorted = sorted(self.word_freq.items(), \
								  key=lambda word: word[1], reverse=True)

	def printMostFreq(self, top_x=20):
		"""
		Prints the most frequent words up until a specified number in a 
		readable table.

		@top_x: The top x number of results to return. By default, it
		returns the top 20 most frequent results
		"""
		# Iterator
		i = 0
		# The table header, so to speak
		print "{0:>15} | {1:>15} | {2:>14}".format("Word", "Total Frequency",\
												   "# of Documents")
		# Goes through the list of sorted words until it reaches the specified
		# limit top_x
		for word in self.word_sorted:
			# Prints out the top x results in a formatted string. In order of
			# Word, Total Frequency, # of Document. word[1] is a 2-list that
			# contains, in this order, the document and total frequency
			print "{0:>15}   {1:15d}  {2:14d}".format(word[0], word[1][1],\
													  word[1][0])
			i += 1
			if i >= top_x: break


		


if __name__ == "__main__":
	# Stemmed text taken from using the stemmer on the content
	# of the page "http://lyle.smu.edu/~jstangelo/IR/test.html"

	doc_text = "there onc wa a man name chicken who hate everyth \
	about himself he wish that he could be a fantast monkei man instead \
	click here to go to test2.html have you seen my sock what the deal \
	with airplan peanut fat chicken man h p faaaart hello i love lasagna"
	doc_id = "doc1"
	doc_dic = {doc_id: doc_text}
	i = Indexer()
	i.indexWords(doc_dic)
	i.word_index
	i.findMostFreq()

