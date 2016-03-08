import re

from urlparse import urlparse
from robotparser import RobotFileParser

class Robot(RobotFileParser, object):

    def __init__(self):
        self.root_path = None
        self.root_finding_regex = r'^\/(.*\/).*$'
        return super(Robot, self).__init__()

    def set_url(self, robots_url):
        """ This function firsts detects if the robots.txt being requested is in
        a location other than the root. If it is, then the current path
        (excluding the robots.txt file) is set as the "root". This allows Robot
        to "fake" non-standard robots.txt locations and treat there path as the
        actual root. Otherwise, this method is the same as
        \code{RobotFileParser}
        """
        url_parts = urlparse(robots_url)
        match = re.match(self.root_finding_regex, url_parts.path)
        if match:
            # e.g. http:lyle.smu.edu/~wspurgin/robots.txt => ~wspurgin
            self.root_path = match.groups()[0]
        return super(Robot, self).set_url(robots_url)

    def can_fetch(self, useragent, url):
        """ If the robots.txt file was at a non-standard location, the url is
        first parse and cleaned to remove the root path associated with the
        robots.txt file (see \code{set_url}). That way the mutated url would be
        be representative of the intentions of the creator of the robots.txt
        file.
        """
        target_url = url
        if self.root_path:
            target_url = re.sub(self.root_path, "", target_url)
        return super(Robot, self).can_fetch(useragent, target_url)


