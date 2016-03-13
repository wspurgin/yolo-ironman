from ironman import Ironman
from parser import Parser
from indexer import Indexer

if __name__ == "__main__":
	fe = Ironman("http://lyle.smu.edu/~fmoore/", treat_as_root=True)
	p = Parser()
	i = Indexer()
	fe.spiderForLinks()
	for soup in fe.good_soup:
		p.retrieveText(soup)
	i.indexWords(p.documents)
	i.printMostFreq