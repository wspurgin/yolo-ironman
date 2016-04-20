#! /usr/bin/env python

from jarvis import Jarvis
from ironman import Ironman
from pepper import Pepper
from urlparse import urlparse
import sys
import os
import re
import operator

class UIQuitException(Exception):
    def __init__(self, *args, **kwargs):
        super(UIQuitException, self).__init__()

class UI(object):

    def __init__(self):
        super(UI, self).__init__()
        self.pepper = None
        self.stop_words = []
        self.top_k = 5

        # Initialize Jarvis
        self.jarvis = Jarvis(stop_words = self.stop_words)

    def loadStopWords(self, stop_words_file_path):
        try:
            with open(stop_words_file_path, 'r') as stop_words_file:
                self.stop_words = [word.strip() for word in stop_words_file.readlines()]
            self.jarvis.stop_words = self.stop_words
        except IOError:
            print "No file found at '%s'" % stop_words_file_path

    def run(self):
        try:
            while(True):
                cmd = ""
                args = []
                raw = raw_input(">")
                try:
                    cmd_and_args = raw.split()
                    cmd, args = (cmd_and_args[0], cmd_and_args[1:])
                    f = operator.methodcaller(cmd, *args)
                except ValueError:
                    cmd = raw
                    f = operator.methodcaller(cmd)
                try:
                    f(self)
                except TypeError as e:
                    # TODO print help doc string for method in cmd.
                    print "Wrong arguments for %s" % cmd
                    print e
                except AttributeError as e:
                    print "No method %s" % cmd
                    print e
        except (UIQuitException, EOFError) as e:
            print
            return

    def quit(self):
        """Exit the interactive session"""
        raise UIQuitException()

    def buildIndex(self, target_url=None, treat_as_root=False, limit=500):
        """Build or add to the Index.
            @usage buildIndex target_url [treat_as_root]
            @param target_url, optional, a full URL (e.g. http://www.smu.edu)
            default is http://lyle.smu.edu/~fmoore/
            @param treat_as_root, optional signifier to treat the given URL as a
            root URL. e.g. treat a URL like, http://lyle.smu.edu/~fmoore/, as
            the root instead of the server instead of http://lyle.smu.edu/
            @param limit, optional limit the underlying crawler to N requests
        """
        # Use ~fmoore as the default target URL.
        if target_url is None:
            target_url = "http://lyle.smu.edu/~fmoore/"
            treat_as_root = True

        # Guard against invalid URLs.
        if not urlparse(target_url).scheme:
            print "Invalid URL: %s" % target_url
            print "HINT: Did you include the scheme? (e.g. http://)"
            return

        # Ensure boolean value safely
        treat_as_root = str(treat_as_root).lower() in ["yes", "y", "true", "t", "1"]

        # Ensure and force Integer value
        try:
            limit = int(limit)
        except ValueError:
            print "Invalid integer value for limit: '%s'" % limit
            print "Using 500 as default"
            limit = 500

        # Start the run
        self.jarvis.run(target_url, treat_as_root, limit)

        # After the run, grab all the necessary objects and output some basic stats
        fe = self.jarvis.ironman
        index = self.jarvis.index
        parser = self.jarvis.parser
        calculator = self.jarvis.calculator
        documents = self.jarvis.documents()

        print "\033[95mCrawl Results\033[0m"
        for category, results in fe.report.iteritems():
            print "\033[94m\t%s:\033[0m" % category
            for crawl in results:
                print"\t%s" % str(crawl)
        print

        # Print out number of unique documents encountered
        print "Encountered %i unique documents" % len(documents)
        print "Removed %i duplicates" % parser.num_duplicates
        print

        # Initialize Pepper to handle queries
        self.pepper = Pepper(documents, calculator, self.stop_words)

    def query(self, *user_query):
        """Run a query against the index
            @usage query user_query...
            @param user_query, a string query of 1 or more words to search
            within the index.
        """
        if self.pepper is None:
            print "Index has not been built! Run `buildIndex` first."
            return
        if len(user_query) == 0:
            print "No query given!"
            return
        else:
            user_query = " ".join(user_query)

        index = self.jarvis.index
        calculator = self.jarvis.calculator

        print "| {0:>15} | {1:>15} | {2:>15} | {3:>14} |".format("Term", "DF", "IDF", "F")
        for term in self.pepper.p.stemText(user_query, self.stop_words).encode('utf_8', 'ignore').split():
            if not index.word_document_frequency.has_key(term): continue
            if not calculator.term_idfs.has_key(term): continue
            if not index.word_freq.has_key(term): continue

            df = index.word_document_frequency[term]
            idf = calculator.term_idfs[term]
            wf = index.word_freq[term]

            print "| {0:>15} | {1:>15d} | {2:>15f} | {3:>14d} |".format(term, df, idf, wf)
        print

        ranked_docs = self.pepper.handleQuery(user_query)
        i = 1
        print "{0:>15} | {1:>15} | {2:>14}".format("Rank", "Score", "Document")
        for score, doc in ranked_docs:
            print "{0:>15} | {1:15f} | {2:14s}".format(i, score, doc.url)
            i += 1
            if i > self.top_k: break

    def setK(self, k=5):
        """Set the number of K results to show in a query (default is 5)
            @usage setK k
            @param k, an integer value representing the number of results to
            show from queries.
        """
        # Ensure and force Integer value
        try:
            k = int(k)
            self.top_k = k
        except ValueError:
            print "Invalid integer value for k: '%s'" % k


if __name__ == "__main__":
    ui = UI()
    ui.loadStopWords(os.path.join(os.path.dirname(__file__), "../stop_words.txt"))
    ui.run()


