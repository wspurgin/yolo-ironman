#!/usr/bin/env python
# Will Spurgin
# 4/23/2014
# yolo-ironman Ironman

import urllib
import requests
import re
import string
import lxml
import sys
import csv

from robotparser import RobotFileParser
from urlparse import urlparse
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
        else:
            self.root = __HTTP__ + "://" + parts.netloc
            self.domain = parts.netloc

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
            self.robot = RobotFileParser()
            self.robot.set_url(self.robots_url)
        self.robot.read()

    def crawl(self, url):
        full_url = self.constructUrl(url)
        is_travelable, reason = self.isTravelable(full_url, include_reason=True)
        # TODO actually handle the return from a crawl...
        if is_travelable:
            req = requests.get(full_url)
            nodeSoup = self.parseSource(req)
            return self.findLinks(nodeSoup, full_url)
        else:
            return (url, reason)

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
        # TODO First check if scheme is supported
        # TODO Check content types?
        url_fragments = urlparse(full_url)
        is_travelable = True
        reason = "valid"

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
        full_url = ""
        url_fragments = urlparse(url)
        current_path = current_url if current_url.endswith("/") else current_url + "/"

        # If the URL doesn't have a scheme (e.g. http, https) then it is a
        # relative address.
        if not url_fragments.scheme:
            # If the tag doesn't start with a slash, it's a relative address
            # from the current page
            if not url.startswith("/"):
                full_url = current_path + url
            else:
                # the url is a relative address from the root, so remove the slash
                path = url[1::]
                full_url = self.root + path
        else:
            full_url = url
        return full_url


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


    # TODO this method still needs refactoring
    def spiderForLinks(self, html, limit=None):
        """
        A breadth-first search on soupified html. Will first scan the page for
        links. If the page is clean, then continue onto a page that this page
        links to, in a breadth-first manner. Stops when the limit is reached or
        no more pages are available
        """
        # Creates a queue of pages to soupify and check for
        # links, and a list of pages already visited, and links to external
        # hosts.
        href_queue = deque([html])
        depth_dict = {html: 0}
        num_pages = 0
        visited_hrefs = []
        external_hrefs = []
        while href_queue:
            # Gets the next link in BFS order
            cur_page = href_queue.popleft()
            # Adds the current page to the pages that have
            # been visited.
            visited_hrefs.append(curPage)
            # Returns the BeautifulSoup of this page. An exception
            # is raised if parseSource tries to open a local file
            # that doesn't exist
            # TODO Handle when the current page is not an HTML file. This should
            # done either here or in parse?
            try:
                cur_soup = self.parseSource(curPage)
            except IOError:
                continue
            # Gets all the links on the page that point
            # to somewhere within the domain. It also checks to
            # see if external links in <script> and <img> tags
            # are flagged by google to be malicious.
            cur_hrefs = self.findLinks(curSoup)

            # Checks to see if any of the found, valid links have
            # already been visited or found
            for href in cur_hrefs:
                if href not in visited_hrefs and href not in href_queue:
                    href_queue.append(href)
                    depth_dict[href] = cur_depth+1

if __name__=="__main__":
    # sample testing
    starting_url = "http://lyle.smu.edu/~fmoore"
    yolo = Ironman(starting_url, treat_as_domain=True)
    nodes = yolo.crawl(starting_url)
    print set(nodes)
