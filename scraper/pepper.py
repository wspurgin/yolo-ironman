#! /usr/bin/env python

from document import Document

class Pepper(object):
	"""
	The Pepper Pots of UI (Public Relations) for Tony Stark. Handles the user
	inputting queries, parsing the queries, and returning results from the
	indexed corpus by Ironman
	"""

	def __init__(self):
		super(Pepper, self).__init__()
		self.queryHandler()

	def queryHandler(self):
		user_input = ""
		