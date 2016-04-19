#! /usr/bin/env python

from document import Document
from normalized_document_calculator import NormalizedDocumentCalculator as N
from porter import PorterStemmer

class Pepper(object):
    """
    The Pepper Pots of UI (Public Relations) for Tony Stark. Handles the user
    inputting queries, parsing the queries, and returning results from the
    indexed corpus by Ironman
    """

    def __init__(self, documents, NDC, stop_words):
        super(Pepper, self).__init__()
        self.documents = documents
        self.NDC = NDC
        self.p = PorterStemmer()
        self.stop_words = stop_words

    def handleQuery(self, user_input):
        """
        Handles the process of formatting a user_inputted query
        """
        scores = []
        stem_query = self.p.stemText(user_input, self.stop_words).encode('utf_8', 'ignore')
        query = Document(user_input, stem_query)
        NDC.normalize(query)
        for document in self.documents:
            scores.append((self.score(query, document), document))
        scores = sorted(self.scores, key=getItem, reverse=True)
        return scores

    def score(query, document):
        return 1

if __name__ == "__main__":
    print "hello"
    full_text = "full text"
    stem_text = "stem text"
    url = "abc"
    hash_id = "123"
    doc = Document(stem_text, full_text, url, hash_id)
    query = Document( stem_text, full_text)
    documents = [doc]
    word_freq = {"full": 1, "text": 1}
    NDC = N(word_freq, 1)
    pe = Pepper(documents, NDC, ["a"])
    print pe.handleQuery("full")