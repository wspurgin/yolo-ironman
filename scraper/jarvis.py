#! /usr/bin/env python

from ironman import Ironman
from parser import Parser
from indexer import Indexer
from urlparse import urlparse
from normalized_document_calculator import NormalizedDocumentCalculator as Calculator
import sys
import pprint
import re

if __name__ == "__main__":
    # If there are only 4 command line arguments, then the first is target URL,
    # the second is the limit on the pages, and the third could either be a file
    # name or a single stop word. In the event of the latter, a message is
    # printed out to the console
    if len(sys.argv) == 4:
        target_url = sys.argv[1]
        limit = sys.argv[2]
        if limit.lower() is "none":
            limit = None
        try:
            with open(sys.argv[3], 'r') as stop_word:
                words = [word.strip() for word in stop_word.readlines()]
        except IOError:
            print "3rd argument not a file. Execution is continuing\
                    assuming it's a stop word"
            words = [sys.argv[3].lower()]
    # If there are greater than 4 command line arguments, then the
    # first is the limit on the pages, and the rest are the stop
    # words that must be considered
    elif len(sys.argv) > 4:
        target_url = sys.argv[1]
        limit = sys.argv[2]
        if limit.lower() == "none":
            limit = None
        words = sys.argv[3:]
    # If there are only 3 command line arguments, then there is only
    # a limit on the pages and no stop words to consider
    elif len(sys.argv) == 3:
        target_url = sys.argv[1]
        limit = sys.argv[2]
        if limit.lower() == "none":
            limit = None
        words = None
    elif len(sys.argv) == 2:
        target_url = sys.argv[1]
        limit = None
        words = None
    # If there are no command line arguements, then there is no limit
    # and no stop words to consider
    else:
        target_url = None
        limit = None
        words = None

    # Use ~fmoore as the default target URL.
    if target_url is None or target_url.lower() == "none":
        target_url = "http://lyle.smu.edu/~fmoore/"

    # Guard against invalid URLs.
    if not urlparse(target_url).scheme:
        print "Invalid URL: %s" % target_url
        print "First argument must be a either 'none' or a valid URL."
        print "HINT: Did you include the scheme? (e.g. http://)"
        quit()

    # Checks to make sure that limit is a valid positive integer before
    # moving on to the next bits
    if limit is not None:
        try:
            limit = int(limit)
            if limit < 0:
                print "Second argument must be either 'none' or a positive integer"
                quit()
        except ValueError:
              if limit != "none":
                print "Second argument must be either 'none' or a positive integer"
                quit()

    treat_as_root = False
    # Check if target url is a non-standard root location.
    url_path = urlparse(target_url).path
    if url_path and re.match(r"^\/([^\.]+)+\/$", url_path):
        treat_as_root = True

    # Creates the ironman object
    fe = Ironman(target_url, treat_as_root=treat_as_root)

    # Creates the parser object, passing in the stop words
    p = Parser(stop_words=words)

    # Creates the indexer object
    i = Indexer()

    # Starts actually crawling through the web page, keeping track of
    # the limit of pages to be accessed
    fe.spiderForLinks(start_url=target_url, limit=limit)
    print "\033[95mCrawl Results\033[0m"
    for category, results in fe.report.iteritems():
        print "\033[94m\t%s:\033[0m" % category
        for crawl in results:
            print"\t%s" % str(crawl)
    print

    # Takes each html, htm, and txt page and extracts all the words, stems
    # all the words, and removes the stop words
    for doc in fe.retrieved_documents:
        url, soup = doc
        p.retrieveText(soup, url)

    # Indexes the words from the documents
    i.indexWords(p.documents)

    # Creates the calculator that will calculate a document's normalized
    # document vector scores. We pass it the word-frequency index throughout
    # the corpus, and the number of documents.
    NDC = Calculator(i.word_freq, len(p.documents))
    
    # Updates every document to hold the normalized term frequency
    for doc in p.documents:
        NDC.normalize(doc)

    
    # # Print out number of unique documents encountered
    # print "Encountered %i unique documents" % len(p.documents)
    # print "Removed %i duplicates" % p.num_duplicates
    # print

    # # Prints out a very pretty table with the most common words
    # i.printMostFreq()
