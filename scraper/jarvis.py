from ironman import Ironman
from parser import Parser
from indexer import Indexer
import sys

if __name__ == "__main__":
	if len(sys.argv == 3):
		limit = argv[1]
		if argv[1].lower() == "none":
			limit = None
		try:
			with open(sys.argv[2], 'r') as stop_word:
				words = stop_word.readlines()
		except IOError:
			print "2nd argument not a file. Execution is continuing\
			 		assuming it's a stop word"
			words = [argv[2].lower()]

	
	elif len(sys.argv > 3):
		limit = argv[1]
		if argv[1].lower() == "none":
			limit = None
		words = argv[2:]

	
	elif len(sys.argv == 2):
		limit = argv[1]
		if argv[1].lower() == "none":
			limit = None
		words = None
	
	else:
		limit = None
		words = None


	fe = Ironman("http://lyle.smu.edu/~fmoore/", treat_as_root=True)
	p = Parser(stop_words=words)
	i = Indexer()
	fe.spiderForLinks(limit=limit)
	for soup in fe.good_soup:
		p.retrieveText(soup)
	i.indexWords(p.documents)
	i.printMostFreq