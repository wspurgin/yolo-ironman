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
        query = Document(stem_query, full_text=user_input)
        self.NDC.normalize(query)
        for document in self.documents:
            scores.append((self.NDC.score(query, document), document))
        scores = sorted(scores, reverse=True)
        return scores

    def score(query, document):
        return 1

if __name__ == "__main__":
    full_text = "full text"
    stem_text = "full text"
    word_freq = {"full": 1, "text": 1}
    url = "abc"
    hash_id = "123"
    NDC = N(word_freq, 1)
    doc = Document(stem_text, full_text, url, hash_id)
    query = Document( stem_text, full_text)

    documents = [doc]
    for d in documents:
        NDC.normalize(d)
    print doc.normalized_tf

    pe = Pepper(documents, NDC, ["a"])
    print pe.handleQuery("full")
