class Crawl(object):

    def __init__(self, url, reason, response):
        self.url = url
        self.reason = reason
        self.response = response

    def tostring(self):
        res = None if not self.response else self.response.status_code
        return "URL: %s Res.: %s Details: %s" % (self.url, str(res), self.reason)

    def __str__(self):
        return self.tostring()

    def __repr__(self):
        return self.tostring()
