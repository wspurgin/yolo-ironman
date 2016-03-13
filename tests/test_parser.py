import context
import requests
import lxml

from unit_test import *
from scraper.parser import *

if __name__=="__main__":

	# Test parser.retreiveText
	subject = "Parser#retreiveText"
	described = Describe(subject)
	test = described.it("Should create a dictionary relating a docID to its page")

	# Set up for tests
	test_url = "http://lyle.smu.edu/~jstangelo/IR/test.html"
	req = requests.get(test_url)
	page_soup1 = BeautifulSoup(req.content, "lxml")
	p = Parser()

	# Run described method
	p.retrieveText(page_soup)