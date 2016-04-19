#! /usr/bin/env python

from document import Document
from normalized_document_calculator import NormalizedDocumentCalculator
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
			scores.append((NDC.score(query, document), document))
		scores = sorted(self.scores, key=getItem, reverse=True)
		return scores