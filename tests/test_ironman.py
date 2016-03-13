import context
from unit_test import *
from scraper.ironman import *

if __name__=="__main__":

    # Test Ironman.constructUrl
    subject = "Ironman#constructUrl"
    described = Describe(subject)

    # test relative addressing
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

    # test relative path resolvement
    test = described.it("should resolve relative positioning in address")
    current_url = starting_url + "/misc/"
    target_url = "../dontgohere"
    resulting_url = yolo.constructUrl(target_url, current_url)
    expected_url = starting_url + "/dontgohere"

    test.expect(resulting_url == expected_url)

    # test external url
    test = described.it("should not alter any external urls")
    target_url = "http://smu.edu/lyle"
    test.expect(yolo.constructUrl(target_url, current_url) == target_url)

    # test it should handle relative address from the root
    test = described.it("should resolve relative addressing from root for non-standard root locations")
    current_url = starting_url + "/misc/silly/programs.html"
    target_url = "/foo"
    expected_url = starting_url + target_url
    resulting_url = yolo.constructUrl(target_url, current_url)
    test.expect(resulting_url == expected_url)

    test = described.it("should resolve relative addressing from root for standard root locations")
    yolo = Ironman(starting_url)
    current_url = starting_url + "/misc/silly/programs.html"
    target_url = "/foo"
    expected_url = "http://lyle.smu.edu" + target_url
    resulting_url = yolo.constructUrl(target_url, current_url)
    test.expect(resulting_url == expected_url)

# ======================== #

    subject = "Ironman#spiderForLinks"
    described = Describe(subject)
    yolo = Ironman(starting_url, treat_as_root=True)

    test = described.it("should take a limit keyword argument that controls how many URLs are visited")
    res = yolo.spiderForLinks(limit=1)
    test.expect(len(res) == 1)

    test = described.it("should populate ironman's intance report and 'good_soup'")
    yolo.spiderForLinks(limit=2)
    test.expect(len(yolo.good_soup) > 0 and len(yolo.report) == 2)
