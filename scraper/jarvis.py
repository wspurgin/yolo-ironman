#! /usr/bin/env python

from ironman import Ironman
from parser import Parser
from indexer import Indexer
from urlparse import urlparse
from normalized_document_calculator import NormalizedDocumentCalculator as Calculator
from pepper import Pepper
import sys
import pprint
import re

class Jarvis(object):

    def __init__(self, stop_words=[]):
        super(Jarvis, self).__init__()

        # Create the parser object, passing in the stop words
        self.parser = Parser(stop_words=stop_words)
        self.index = Indexer()
        self.calculator = None
        self.stop_words = stop_words
        self.ironman = None

    def run(self, target_url, treat_as_root=False, limit=500):
        # Create the ironman object
        self.ironman = Ironman(target_url, treat_as_root=treat_as_root)

        # Starts crawling through the web page, keeping track of the limit of pages
        # to be accessed
        self.ironman.spiderForLinks(start_url=target_url, limit=limit)

        # Takes each html, htm, and txt page and extracts all the words, stems
        # all the words, and removes the stop words
        for doc in self.ironman.retrieved_documents:
            url, soup = doc
            self.parser.retrieveText(soup, url)

        documents = self.documents()

        # Indexes the words from the documents
        self.index.indexWords(documents)

        # Creates the calculator that will calculate a document's normalized
        # document vector scores. We pass it the word-frequency index throughout
        # the corpus, and the number of documents.
        self.calculator = Calculator(self.index.word_document_frequency,
                len(documents))

        # Updates every document to hold the normalized term frequency
        for doc in documents:
            self.calculator.normalize(doc)

    def documents(self):
        return self.parser.documents

