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
from document import Document

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
        self.hashes = []
        self.documents = []
        self.num_duplicates = 0
        self.p = PorterStemmer()

    def retrieveText(self, page_soup, url):
        """
        Retrieves all the non-markup text from a webpage that
        has already been crawled.

        @page_soup: The soupified version of a webpage
        """
        # Retrieve all the text of the page minus the html tags
        page_text = page_soup.get_text()
        # Stems and returns all the non-stopword text
        stem_text = self.p.stemText(page_text, self.stop_words).encode('utf_8', 'ignore')
        # Create a hash to make sure there are no 100% duplicates in the pages
        # The hex digest will also be used as the document ID, since they will
        # be unique unless they are a duplicate
        h = hashlib.md5()
        h.update(stem_text)
        page_hash = h.hexdigest()
        # If the page is not a duplicate, add the hash to a list of found
        # hashes, and create a Document object to keep track of the information
        # for each Document
        if page_hash not in self.hashes:
            self.hashes.append(page_hash)
            self.documents.append(Document(stem_text, page_text, url, page_hash))
        else:
            self.num_duplicates += 1

if __name__ == "__main__":
    test_url = "http://lyle.smu.edu/~jstangelo/IR/test.html"
    req = requests.get(test_url)
    page_soup = BeautifulSoup(req.content, "lxml")
    p = Parser(None)
    p.retrieveText(page_soup, test_url)
    print p.documents[0].full_text
    print p.documents[0].stem_text