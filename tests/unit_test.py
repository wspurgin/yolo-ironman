class Describe(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self, subject):
        self.subject = subject
        self.failures = 0
        self.successes = 0
        print self.HEADER + self.UNDERLINE + subject + self.ENDC

    def it(self, should):
        return self.Test(self, "it " + should)

    class Test(object):

        def __init__(self, describer, expectation):
            self.describer = describer
            self.expectation = expectation

        def expect(self, test):
            result = ""
            if test:
                self.describer.successes += 1
                result =  " (Passed %i)" % self.describer.successes
                print self.describer.OKGREEN
            else:
                self.describer.failures += 1
                result =  " (Failed %i)" % self.describer.failues
                print self.describer.FAIL
            print self.expectation + result + self.describer.ENDC

