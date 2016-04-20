#!/usr/bin/env python
# Will Spurgin
# Joe St. Angelo
# yolo-ironman Ironman

import urllib
import requests
import re
import string
import lxml
import sys
import time

from robot import Robot
from crawl import Crawl
from urlparse import urlparse, urljoin
from bs4 import BeautifulSoup
from collections import deque

# "constants"
__ROBOTS_TXT__ = "/robots.txt" # relative address of robots.txt from host
__USER_AGENT__ = "*"           # user agent to check in robots.txt
__HTTP__       = "http"

class Ironman(object):
    """
    The Tony Stark of web crawler classes. Yolo.
    @param starting_url
    @param treat_as_root = false

    The `treat_as_root` option is useful if the starting URL is not actually a
    root but you want Ironman to treat it like it is, such as
    http://lyle.smu.edu/~wspurgin
    """

    def __init__(self, starting_url, treat_as_root=False, **kwargs):
        super(Ironman, self).__init__()
        self.treat_as_root = treat_as_root
        self.report = {}
        self.retrieved_documents = []
        self.robot = None

        # Test staring URL for redirect
        res = requests.head(starting_url, allow_redirects=True)
        if res.url != starting_url:
            print "Starting URL '%s' Redirected to: %s" % (starting_url, res.url)
            if treat_as_root:
                print "`treat_as_root` flag will be forced to off."
                self.treat_as_root = False
            self.starting_url = res.url
        else:
            self.starting_url = starting_url

        parts = urlparse(self.starting_url)
        if self.treat_as_root:
            self.root = self.starting_url
            path = parts.path
            if path.endswith("/"):
                path = path[0:-1]
            self.domain = parts.netloc + path
            self.root_path = path
            if not self.root_path.endswith("/"):
                self.root_path += "/"
        else:
            self.root = __HTTP__ + "://" + parts.netloc
            self.domain = parts.netloc
            self.root_path = "/"

        # Add an ending slash to the root if it doesn't already have one. This
        # doesn't affect the URL results, but helps when having to deal with
        # relative addresses.
        if not self.root.endswith("/"):
            self.root += "/"

        # Get Robots.txt and parse it for information.
        self.robots_url = self.constructUrl(__ROBOTS_TXT__)
        self.updateRobots()

    def updateRobots(self):
        if self.robot is None:
            self.robot = Robot()
            self.robot.set_url(self.robots_url)
        self.robot.read()

    def crawl(self, url):
        full_url = self.constructUrl(url)
        is_travelable, reason = self.isTravelable(full_url, include_reason=True)
        req = None
        if is_travelable:
            req = requests.head(full_url, allow_redirects=True)
        return Crawl(full_url, reason, req)

    def isTravelable(self, full_url, include_reason=False):
        """
        Determines if the given url is "travelable". This is based on looking at
        URL scheme (e.g. http, sftp, mailto, etc.), and then if it is an HTTP(S)
        URL, the robots.txt file rules are used to determine if Ironman is
        allowed to retrieve the URL.

        @param full_url, This is the URL to examine. It should be a fully valid
        URL (e.g. http://google.com). Use `constructUrl` if unsure if the URL is
        a fully valid URL.

        @returns a tuple of (is_travelable:boolean, reason:string)
        """
        url_fragments = urlparse(full_url)
        is_travelable = True
        reason = "Valid URL"
        if not self.robot.can_fetch(__USER_AGENT__, full_url):
            is_travelable = False
            reason = "Robots.txt Disallowed"
        elif url_fragments.scheme != "http" and url_fragments.scheme != "https":
            is_travelable = False
            reason = "Unsupported scheme %s" % url_fragments.scheme
        else:
            if self.isExternal(full_url):
              is_travelable = False
              reason = "External URL"

        if include_reason:
            return (is_travelable, reason)
        else:
            return is_travelable

    def isExternal(self, url):
          if self.treat_as_root:
            url_without_scheme = re.sub(r'https?:\/\/', "", url)
            if not url_without_scheme.startswith((self.domain)):
                return True
          else:
            if urlparse(url).netloc != self.domain:
                return True

    def constructUrl(self, url, current_url=None):
        """
        Creates a URL for when the given URL is a relative path to another page
        on the same site. Examples of possible hrefs:
            newPage.html
            /pageInRootFolder.html
            /folderInRootFolder/newSubfolder/newPage.html
            ../differentFolder/newPage.html
            ../../differentFolder/otherFolder/newPage.html
        """
        # Guard statement for if current_url is not given.
        current_url = self.root if not current_url else current_url
        target_url = url
        if target_url.startswith("/") and self.treat_as_root:
            # The target url is relative from root, and we have a non-standard
            # root location
            target_url = self.root_path + url[1::]

        return urljoin(current_url, target_url)


    def parseSource(self, source):
        """
        Takes in a Requests HTTP request object. A BeautifulSoup object is
        returned.
        """
        # TODO Use different parser based on content types?
        source = source.content
        return BeautifulSoup(source, "lxml")

    def findLinks(self, html_soup, current_url):
        """
        Takes in a BeautifulSoup object from a soupified url. Searches through
        a webpage and returns all the links on the page.
        """
        # Finds all the tags in the soup, and stores only the href
        # and src attributes.
        links = []
        tags = html_soup.find_all(href=True) + html_soup.find_all(src=True)
        for tag in tags:
            if tag.get('href') is not None:
                links.append(tag['href'])
            elif tag.get('src') is not None:
                links.append(tag['src'])
        links = [ self.constructUrl(link, current_url) for link in links ]

        return links

    def getDomain(self, url):
        """
        This will allow for easy comparisons of whether a link is external or not.
        """
        return urlparse(url).netloc

    def isParsableContentType(self, content_type):
      types = [r"text\/html", r"text\/plain", r"text\/xml"]
      parsable = False
      for type in types:
          parsable = bool(re.match(type, content_type))
          if parsable:
              break
      return parsable


    def spiderForLinks(self, start_url=None, limit=None, politeness_factor=2):
        """
        A breadth-first search on soupified html. Will first scan the page for
        links. If the page is clean, then continue onto a page that this page
        links to, in a breadth-first manner. Stops when the limit is reached or
        no more pages are available
        """
        # Creates a queue of pages to soupify and check for
        # links, and a list of pages already visited, and links to external
        # hosts.
        start_url = self.constructUrl(self.starting_url if not start_url else start_url)
        href_queue = deque([start_url])
        visited_hrefs = []
        self.report = {}
        self.retrieved_documents = []
        requests_made = 0
        last_request_time = 0
        while href_queue:
            # Guard statement to ensure we observe a limit (if one is given).
            if limit and requests_made == limit:
                break

            # Politely give the server a break from our bombardment based on
            # politeness_factor
            time.sleep(politeness_factor * last_request_time)

            # Gets the next link in BFS order
            cur_url = href_queue.popleft()
            crawl = self.crawl(cur_url)
            full_url, reason, response = [crawl.url, crawl.reason, crawl.response]

            # Adds the current page to the pages that have
            # been visited.
            visited_hrefs.append(full_url)
            sys.stdout.write("\rNumber of pages visited: %d" % len(visited_hrefs))
            sys.stdout.flush()

            # There may be no response if a request was never attempted (e.g.
            # it was an external link)
            if response is None:
              # Ensure report has a spot for the results
              if reason not in self.report:
                  self.report[reason] = []
              self.report[reason].append(crawl)
              continue

            last_request_time = response.elapsed.total_seconds()
            requests_made += 1

            skip = False
            if response.status_code != requests.codes.ok:
              crawl.reason = "Returned %i" % response.status_code
              skip = True
            elif not self.isParsableContentType(response.headers['content-type']):
              crawl.reason = "Does not have a parsable content type: %s" % response.headers["content-type"]
              skip = True
            elif response.url != full_url and response.url in visited_hrefs:
              # We've been redirected to a location that we've already visited
              # so it's safe to skip
              crawl.reason = "Redirected to already visited URL"
              skip = True
            elif self.isExternal(response.url):
              crawl.reason = "Redirected to External URL: %s" % response.url
              skip = True

            if not skip:
              #  lxml will raise a Syntax error if the document is malformed
              try:
                  # we have a parsable content type, so we have to retreive the
                  # document.
                  cur_soup = self.parseSource(requests.get(response.url))
              except lxml.etree.XMLSyntaxError as e:
                  crawl.reason = "Parsing content failed with an \
                      exception: " + str(e)
                  skip = True

            # Ensure report has a spot for the results
            if crawl.reason not in self.report:
                self.report[crawl.reason] = []
            self.report[crawl.reason].append(crawl)

            if skip:
                continue

            # Gets all the links on the page that point
            # to somewhere within the domain. It also checks to
            # see if external links in <script> and <img> tags
            # are flagged by google to be malicious.
            cur_hrefs = self.findLinks(cur_soup, response.url)
            self.retrieved_documents.append((full_url, cur_soup))

            # Checks to see if any of the found, valid links have
            # already been visited or found
            for href in cur_hrefs:
                if href not in visited_hrefs and href not in href_queue:
                    href_queue.append(href)
        return self.report

