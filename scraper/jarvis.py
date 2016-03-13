from ironman import Ironman
from parser import Parser
from indexer import Indexer
import sys

if __name__ == "__main__":
    # If there are only 3 command line arguments, then the first is 
    # the limit on the pages, and the second could either be a file
    # name or a single stop word. In the event of the latter, a
    # message is printed out to the console
    if len(sys.argv) == 3:
        limit = sys.argv[1]
        if limit.lower() is "none":
            limit = None
        try:
            with open(sys.argv[2], 'r') as stop_word:
                words = stop_word.readlines()
        except IOError:
            print "2nd argument not a file. Execution is continuing\
                    assuming it's a stop word"
            words = [sys.argv[2].lower()]
    # If there are greater than 3 command line arguments, then the
    # first is the limit on the pages, and the rest are the stop 
    # words that must be considered
    elif len(sys.argv) > 3:
        limit = sys.argv[1]
        if limit.lower() == "none":
            limit = None
        words = sys.argv[2:]
    # If there are only 2 command line arguments, then there is only
    # a limit on the pages and no stop words to consider    
    elif len(sys.argv) == 2:
        limit = sys.argv[1]
        if limit.lower() == "none":
            limit = None
        words = None
    # If there are no command line arguements, then there is no limit
    # and no stop words to consider
    else:
        limit = None
        words = None
    # Checks to make sure that limit is a valid positive integer before
    # moving on to the next bits
    if limit is not None:
        try:
            limit = int(sys.argv[1])
            if limit < 0:
                print "First argument must be either 'none' or a positive integer"
                quit()
        except ValueError:
            print "First argument must be either 'none' or a positive integer"
            quit()
    # Creates the ironman object
    fe = Ironman("http://lyle.smu.edu/~fmoore/", treat_as_root=True)
    # Creates the parser object, passing in the stop words
    p = Parser(stop_words=words)
    # Creates the indexer object
    i = Indexer()
    # Starts actually crawling through the web page, keeping track of 
    # the limit of pages to be accessed
    fe.spiderForLinks(limit=limit)
    # Takes each html, htm, and txt page and extracts all the words, stems
    # all the words, and removes the stop words
    for soup in fe.good_soup:
        p.retrieveText(soup)
    # Indexes the words from the documents
    i.indexWords(p.documents)
    # Prints out a very pretty table with the most common words
    i.printMostFreq()