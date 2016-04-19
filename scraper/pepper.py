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

	def __init__(self, documents, NDC):
		super(Pepper, self).__init__()
		self.documents = documents
		self.NDC = NDC
		self.p = PorterStemmer()
		self.handleQuery()

	def handleQuery(self, user_input):
	"""
	Handles the process of formatting a user_inputted query
	"""
		stem_query = self.p.stemText(user_input).encode('utf_8', 'ignore')
		query = Document(user_input, stem_query)
		NDC.normalize(query)
		
