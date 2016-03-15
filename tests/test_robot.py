import context
from unit_test import *
from scraper.robot import *

if __name__=="__main__":
    subject = "Robot"
    described = Describe(subject)

    # test  addressing
    test = described.it("should allow for non-standard locations of robots.txt")
    r = Robot()
    r.set_url("http://lyle.smu.edu/~fmoore/robots.txt")
    r.read()
    test.expect(not r.can_fetch("*", "http://lyle.smu.edu/~fmoore/dontgohere/badfile1.htm"))

