# Will Spurgin
# Joe St. Angelo
# Yolo-Ironman

class Document(object):
	"""
	The document object that will keep track of all the relevant info
	for each document that the crawler comes across. Used especially
	specifically to make indexing and searching an easier and quicker
	process.
	"""

	def __init__(self, full_text, stem_text, url=None, hash_id=None):
		super(Document, self).__init__()
		self.url = url
		self.full_text = full_text
		self.stem_text = stem_text
		self.id = hash_id
		text_list = stem_text.split()
		self.word_vector = {x:text_list.count(x) for x in text_list}
                self.normalized_tf = {}
