#!/usr/local/bin/python
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

class Ironman(object):
    """
    The Tony Stark of web crawler classes. Yolo.
    @param starting_url
    @param treat_as_host = false
    @kwargs
        bind_to_starting_host = boolean

    The `treat_as_host` option is useful if the starting URL is not actually a
    host but you want Ironman to treat it like it is, such as
    http://lyle.smu.edu/~wspurgin
    """
    def __init__(self, starting_url, treat_as_host=False, **kwargs):
        super(Ironman, self).__init__()
        self.starting_url = starting_url
        self.treat_as_host = treat_as_host
        self.externalLinks = []
        if self.treat_as_host:
            self.host = self.starting_url
        else:
            self.host = urlparse(self.starting_url).netloc
        self.pattern = re.compile('<a\s?.*href="(.+\w+)"\s*>', re.IGNORECASE)
        if 'pattern' in kwargs:
            self.pattern = re.compile(kwargs['pattern'], re.IGNORECASE)

        # Get Robots.txt and parse it for information.

    def crawl(self):
        if not self.starting_url:
            raise Exception("No url set for instance of Ironman")
        nodeSoup = self.parseSource(self.starting_url)
        self.findPages(nodeSoup, self.host, self.starting_url, )

    def parseSource(self, url):
        """
        Takes in a URL or a local path to either a webpage
        that needs to be tested, or a local document that
        is either a webpage or file with malware. A BeautifulSoup
        object is returned in either case, along with a string
        to indicate whether it is a url or file path.
        """
        # If url is actually a URL, then it needs to be
        # opened with requests, otherwise it's a local
        # file path, which can be opened the 'normal' way
        source = requests.get(url)
        source = source.content

        # TODO Check content types

        return BeautifulSoup(source, "html.parser")

    def createList(self, soup, tags=True):
        """
        Takes in a BeautifulSoup object from a soupified
        file, and a list of tags to search for. It first
        creates a list of the tags. It then iterates over
        the list, removing white space from the text inside
        of the tags in order for comparisons between lists
        from different sources to give false negatives.
        """
        soupList = [tag for tag in soup.find_all(tags)]
        for idx, tag in enumerate(soupList):
            # tag.string returns None if there is no text inside the tag
            if tag.string:
                # Replaces the string inside the tags with the same string
                # without ANY white space.
                # http://stackoverflow.com/questions/3739909/how-to-strip-all-whitespace-from-string
                soupList[idx].string.replace_with("".join(tag.string.split()))
        return soupList

    def findPages(self, htmlSoup, domainUrl, currentUrl, savingPages=False):
        """
        Takes in a BeautifulSoup object from a soupified url,
        and the domainUrl of that website. Searches through a
        webpage searching for all the links on the page, and
        then whittling it down to only links that are on the
        original URL's domain. It will also check to see if
        the src attributes of img and script tags to external
        domains is flagged by google to be malicious.
        """
        # Finds all the tags in the soup, and stores only the href
        # and src attributes.
        tagList = []
        for tag in htmlSoup.find_all(True):
            if tag.get('href') is not None:
                tagList.append(tag['href'], tag)
            elif tag.get('src') is not None:
                tagList.append(tag['src'], tag)

        # tempList = [(tag['href'], tag) for tag in htmlSoup.find_all(True) if tag.get('href') is not None]
        # Removes all links not on the correct domain, and creates
        # urls based off of relative paths.
        hrefList = []
        for tag in tagList:
            # If the href is to a page on the same domain as the
            # current page.
            if getDomain(tag[0]) == domainUrl:
                hrefList.append(tag[0])
            # If the href is a relative path.
            elif string.find(tag[0][:4], 'http') == -1:
                hrefList.append(constructUrl(tag[0], currentUrl))
            # The href is to a page on a different domain.
            else:
                self.externalLinks.append(tag[0])
        return hrefList

    def constructUrl(self, tag, currentUrl):
        """
        Creates a URL for when an anchor tag has an href
        attribute that is a relative path to another page
        on the same site. Examples of possible hrefs:
            newPage.html
            /pageInRootFolder.html
            /folderInRootFolder/newSubfolder/newPage.html
            ../differentFolder/newPage.html
            ../../differentFolder/otherFolder/newPage.html
        """
        currentPath = string.rsplit(currentUrl, '/', 1)[0] + '/'
        slashLoc = string.find(tag, '/')
        # If the tag doesn't have any slashes, it's to a new page
        # in the same directory as the current page
        if slashLoc == -1:
            return currentPath + tag
        # If the tag starts with a slash, then it is relative to
        # the root directory of the website
        # TODO don't manually add URL schema, use the one initalized in
        # construction
        elif slashLoc == 0:
            return 'http://' + getDomain(currentPath) + tag
        # If the tag starts with '../', then it is one folder up
        # from the current path. There can be any number of '../'
        # at the start of the path, so it must account for all of
        # them
        else:
            folders = string.count(tag, '../')
            return string.rsplit(currentPath, '/', folders+1)[0] + '/' + string.lstrip(tag, '../')


    def getDomain(self, url):
        """
        Utilizes Marie's domainGetter file to extract the registered
        domain from the url. This will allow for easy comparisons
        of whether a link is external or not.
        """
        return urlparse(url).netloc


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
        hrefQueue = deque([html])
        depthDict = {html: 0}
        numPages = 0
        visitedHrefs = []
        externalHrefs = []
        while hrefQueue:
            # Gets the next link in BFS order
            curPage = hrefQueue.popleft()
            # Adds the current page to the pages that have
            # been visited.
            visitedHrefs.append(curPage)
            # Returns the BeautifulSoup of this page. An exception
            # is raised if parseSource tries to open a local file
            # that doesn't exist
            # TODO Handle when the current page is not an HTML file. This should
            # done either here or in parse?
            try:
                curSoup = parseSource(curPage)
            except IOError:
                continue
            # Gets all the links on the page that point
            # to somewhere within the domain. It also checks to
            # see if external links in <script> and <img> tags
            # are flagged by google to be malicious.
            curHrefs = findPages(curSoup, domainUrl, curPage)

            # Checks to see if any of the found, valid links have
            # already been visited or found
            for href in curHrefs:
                if href not in visitedHrefs and href not in hrefQueue:
                    hrefQueue.append(href)
                    depthDict[href] = curDepth+1

if __name__=="__main__":
    # sample testing
    starting_url = "http://lyle.smu.edu/~fmoore"
    yolo = Ironman(starting_url, treat_as_host=True)
    nodes = yolo.crawl()
    print set(nodes)
