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
from document import Document
from operator import itemgetter
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
        # Contains the index of word to documents
        self.word_index = {}
        # Keeps track of the total frequency. Keeps track of
        # number of total occurences throughout the corpus.
        self.word_freq = {}
        self.word_sorted = []

    def indexWords(self, documents):
        """
        Reads each word in the dociment_dic and creates an inverse doc list
        with also its frequency in that document. The inverse doc is a
        dictionary that relates each word to a list that contains tuples of the
        docID, and the frequency of that word in that doc.
        E.g.
        the => [(doc1, 4), (doc2, 3), (doc3, 6)]
        banana => [(doc1, 1), (doc3, 1)]
        """
        # Goes through all the documents in the list
        for document in documents:
            # Goes through each word in the document
            for word in document.word_vector:
                # If that word has not been found
                if word not in self.word_index:
                    # Add the word to the index, and relate it to a list
                    # containing the document object that it was first 
                    # found in. 
                    self.word_index[word] = [document]
                    # Add the word to the word frequency list and
                    # set its value to the number of times appears 
                    # in this document.
                    self.word_freq[word] = document.word_vector[word]
                else:
                    # Add this document to the list of documents that
                    # have this word in it
                    self.word_index[word].append(document)
                    # Updates the number of times this word appears in the
                    # corpus by the number of times it appears in this
                    # document
                    self.word_freq[word] += document.word_vector[word]
       
        self.word_sorted = sorted(self.word_freq.iteritems(), key=itemgetter(1), reverse=True)
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
            print "{0:>15}   {1:15d}  {2:14d}".format(word[0], word[1], \
                                            len(self.word_index[word[0]]))
            i += 1
            if i >= top_x: break





if __name__ == "__main__":
    # Stemmed text taken from using the stemmer on the content
    # of the page "http://lyle.smu.edu/~jstangelo/IR/test.html"

    doc_text = "there onc wa a man name chicken who hate everyth \
    about himself he wish that he could be a fantast monkei man instead \
    click here to go to test2.html have you seen my sock what the deal \
    with airplan peanut fat chicken man h p hello i love lasagna"
    doc_id = "doc1"
    doc_url = "www.abc.com"
    d = [Document(doc_text, doc_url, doc_id)]
    i = Indexer()
    i.indexWords(d)
    #print i.word_index
    #print i.word_freq
    i.printMostFreq()

