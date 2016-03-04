import context
from unit_test import *
from scraper.ironman import *

if __name__=="__main__":

    # Test Ironman.constructUrl
    subject = "Ironman#constructUrl"
    described = Describe(subject)
    test = described.it("should construct relative address from current url")

    # Set up test variables
    starting_url = "http://lyle.smu.edu/~fmoore"
    current_url = starting_url + "/index.htm"
    target_url = "schedule.htm"

    # Set up Ironman object to perform test
    yolo = Ironman(starting_url, treat_as_root=True)

    # Run described method
    resulting_url = yolo.constructUrl(target_url, current_url)
    expected_url = starting_url + "/" + target_url

    test.expect(resulting_url == expected_url)

