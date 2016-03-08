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
import csv
import pprint

from robot import Robot
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
        self.starting_url = starting_url
        self.treat_as_root = treat_as_root
        self.external_links = []
        self.robot = None

        parts = urlparse(self.starting_url)
        if self.treat_as_root:
            self.root = self.starting_url
            self.domain = parts.netloc + parts.path
            self.root_path = parts.path
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
        # TODO actually handle the return from a crawl...
        req = None
        if is_travelable:
            req = requests.get(full_url)
        return (full_url, reason, req)

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
        reason = "valid"
        # TODO when the root/domain is non standard (like
        # lyle.smu.edu/~wspurgin) and the robots.txt is meant to disallow
        # directories like "/dontgohere" from that non standard root, the robot
        # will think it means "lyle.smu.edu/dontgohere" not
        # "lyle.smu.edu/~wspurgin/dontgohere"
        if not self.robot.can_fetch(__USER_AGENT__, full_url):
            is_travelable = False
            reason = "Robots.txt Disallowed"
        elif url_fragments.scheme != "http" and url_fragments.scheme != "https":
            is_travelable = False
            reason = "Unsupported scheme %s" % url_fragments.scheme
        else:
          if self.treat_as_root:
            url_without_scheme = re.sub(r'https?:\/\/', "", full_url)
            if not url_without_scheme.startswith((self.domain)):
              is_travelable = False
              reason = "External URL"
          else:
            if url_fragments.netloc == self.domain:
              is_travelable = False
              reason = "External URL"

        if include_reason:
            return (is_travelable, reason)
        else:
            return is_travelable

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
            target_url = self.root_path + url

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

    def parsableContentTypes(self):
      return ["text/html", "text/plain", "text/xml"]


    # TODO this method still needs refactoring
    def spiderForLinks(self, start_url=None, limit=None):
        """
        A breadth-first search on soupified html. Will first scan the page for
        links. If the page is clean, then continue onto a page that this page
        links to, in a breadth-first manner. Stops when the limit is reached or
        no more pages are available
        """
        # Creates a queue of pages to soupify and check for
        # links, and a list of pages already visited, and links to external
        # hosts.
        start_url = self.root if not start_url else start_url
        href_queue = deque([start_url])
        num_pages = 0
        visited_hrefs = []
        external_hrefs = []
        report = {}
        while href_queue:
            # Gets the next link in BFS order
            cur_url = href_queue.popleft()
            full_url, reason, request = self.crawl(cur_url)

            # Adds the current page to the pages that have
            # been visited.
            visited_hrefs.append(full_url)

            # Add to report
            report[full_url] = reason

            # Returns the BeautifulSoup of this page. An exception
            # is raised if parseSource tries to open a local file
            # that doesn't exist
            if request is None:
              continue
            elif request.status_code != requests.codes.ok:
              report[full_url] = "Returned %i" % request.status_code
              # TODO add to bad url list for accounting purposes?
              continue
            elif request.headers['content-type'] not in self.parsableContentTypes():
              report[full_url] = "Does not have a parsable content type"
              # TODO add to bad url list for accounting purposes?
              continue
            try:
                cur_soup = self.parseSource(request)
            except IOError:
                continue
            # Gets all the links on the page that point
            # to somewhere within the domain. It also checks to
            # see if external links in <script> and <img> tags
            # are flagged by google to be malicious.
            cur_hrefs = self.findLinks(cur_soup, full_url)

            # Checks to see if any of the found, valid links have
            # already been visited or found
            for href in cur_hrefs:
                if href not in visited_hrefs and href not in href_queue:
                    href_queue.append(href)
        return report

