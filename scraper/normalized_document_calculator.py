from math import log10, sqrt

# Yolo-Ironman imports
from document import Document

class NormalizedDocumentCalculator(object):
    """A calculator to get a document's normalized document vector scores"""
    def __init__(self, term_freqs, number_of_documents):
        super(NormalizedDocumentCalculator, self).__init__()
        self.term_freqs = term_freqs
        self.number_of_documents = number_of_documents
        self.term_idfs = {}
        self.calculateTermIdfs()

    def calculateTermIdfs(self):
        N = self.number_of_documents
        for term in self.term_freqs:
            self.term_idfs[term] = log10(N / self.term_freqs[term])

    def normalize(self, doc):
        if type(doc) is not Document:
            raise ValueError("NormalizedDocumentCalculator.normalize expects a Document object")

        # Perform Idf weighting of term frequencies on the doc.
        for term in doc.word_vector:
            doc.normalized_tf[term] = doc.word_vector[term] * self.term_idfs[term]

        # Caculate the Euclidean distance for the weighted document vector.
        euclidean_dist = 0.0
        for val in doc.normalized_tf.values():
            euclidean_dist+= pow(val, 2)
        euclidean_dist = sqrt(euclidean_dist)

        # Normalize the weighted document vector with the L2 norm (i.e. divide
        # each term by the euclidean distance).
        for term, wf in doc.normalized_tf.items():
            doc.normalized_tf[term] = wf / euclidean_dist

