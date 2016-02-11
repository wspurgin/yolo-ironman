from bs4 import BeautifulSoup
import string
import domainGetter as dg
from collections import deque
import re
import lxml
import requests
import malwares
import sys
import csv

def readInputFile(urlFile = 'scanList.txt'):
    urlList = []
    fl = open(urlFile, 'r')
    for url in fl:
        urlList.append(url)
    fl.close()
    return urlList

def readStatFile():
    fl = open('stats.csv', 'r')
    reader = csv.reader(fl)
    statDict = {}
    for row in reader:
        statDict[row[0]] = (row[1], row[2])
    fl.close()
    return statDict

def writeStateFile(statDict, statFile):
    fl = open(statFile, 'w')
    writer = csv.writer(fl, delimiter=',')
    for url, dates in statDict.iteritems():
        writer.writerow([url, dates[0], dates[1]])
    fl.close()

def parseSource(url):
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
    if string.find(url[:4], "http") != -1:
        try:
            fName = '../Test/TestSite/'+url.replace('/', '')
            if (len(fName)>235):
                fName = fName[:235]
            fl = open('../Test/TestSite/'+url.replace('/', ''))
            source = fl.read()
            fl.close()
        except IOError:
            source = requests.get(url)
            #if malwares.htaccess(source.headers, url): 
            #    return 'redirect'
            source = source.content
    else:
        fl = open(url, 'r')
        source = fl.read()
        fl.close()
    return BeautifulSoup(source, "html.parser")

def createList(soupObj, tags=True):
    """
    Takes in a BeautifulSoup object from a soupified
    file, and a list of tags to search for. It first 
    creates a list of the tags. It then iterates over 
    the list, removing white space from the text inside 
    of the tags in order for comparisons between lists 
    from different sources to give false negatives.
    """
    soupList = [tag for tag in soupObj.find_all(tags)]
    for idx, tag in enumerate(soupList):
        # tag.string returns None if there is no text inside
        # the tag
        if tag.string:
            # Replaces the string inside the tags with the
            # same string without ANY white space.
            # http://stackoverflow.com/questions/3739909/how-to-strip-all-whitespace-from-string
            soupList[idx].string.replace_with("".join(tag.string.split()))
    return soupList

def findPages(htmlSoup, domainUrl, currentUrl, savingPages=False):
    """
    Takes in a BeautifulSoup object from a soupified url,
    and the domainUrl of that website. Searches through a 
    webpage searching for all the links on the page, and 
    then whittling it down to only links that are on the
    original URL's domain. It will also check to see if
    the src attributes of img and script tags to external
    domains is flagged by google to be malicious.
    """
    regex = '(\.html$|\.htm$|\.js$|\.php$|\.css$|\.aspx$|\/$|\/([^\.]+)$)'
    # Finds all the tags in the soup, and stores only the href
    # and src attributes.
    tagList = []
    for tag in htmlSoup.find_all(True):
        if tag.get('href') is not None:
            tagList.append(tag['href'], tag)
        elif tag.get('src') is not None:
            tagList.append(tag['src'], tag)

    #tempList = [(tag['href'], tag) for tag in htmlSoup.find_all(True) if tag.get('href') is not None] 
    # Removes all links not on the correct domain, and creates
    # urls based off of relative paths.
    hrefList = []
    for tag in tagList:
        # If the page that's being linked to is not a page that
        # interests us, then it is skipped over.
        if not re.search(regex, tag[0]): continue
        # If the href is to a page on the same domain as the
        # current page.
        if getDomain(tag[0]) == domainUrl:
            hrefList.append(tag[0])
        # If the href is a relative path. 
        elif string.find(tag[0][:4], 'http') == -1:
            hrefList.append(constructUrl(tag[0], currentUrl))
        # If the href is to a page on a different domain, and
        # the href is contained in either a <script> or <img>
        elif (tag[1] == 'script' or tag[1] == 'img') and malwares.googleFlagged(tag[0]) and not savingPages:
            return (tag)
    return hrefList

def constructUrl(tag, currentUrl):
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
    elif slashLoc == 0:
        return 'http://' + getDomain(currentPath) + tag
    # If the tag starts with '../', then it is one folder up
    # from the current path. There can be any number of '../'
    # at the start of the path, so it must account for all of
    # them
    else:
        folders = string.count(tag, '../')
        return string.rsplit(currentPath, '/', folders+1)[0] + '/' + string.lstrip(tag, '../')


def getDomain(url):
    """
    Utilizes Marie's domainGetter file to extract the registered
    domain from the url. This will allow for easy comparisons
    of whether a link is external or not.
    """
    return dg.gettld(url)

def crawlForMalware(html):
    """
    Scans a single webpage for malware.
    """
    soup = parseSource(html)
    if soup == 'redirect' or malwares.findMalware(soup):
        print "Malware found on", html
        return True
    else:
        return False

def spiderForMalware(html):
    """
    A breadth-first search on soupified html. Will first
    scan the page for malware. If the page is clean, then
    continue onto a page that this page links to, in a 
    breadth-first manner. Stops when either a page has
    been found to have malware, or the depth of the search
    exceeds 5 layers.
    """
    # Returns the domain of a given URL. We only want to
    # go to other pages on the same domain
    domainUrl = getDomain(html)
    # Creates a queue of pages to soupify and check for
    # malware, and a list of pages already visited.
    hrefQueue = deque([html])
    depthDict = {html: 0}
    numPages = 0
    visitedHrefs = []
    while hrefQueue:
        # Gets the next link in BFS order
        curPage = hrefQueue.popleft()   
        curDepth = depthDict[curPage]
        # Once the depth reaches 3, then we are assuming 
        # that the website is clean
        if curDepth > 1: 
            print "Maximum depth reached"
            break
        # Adds the current page to the pages that have
        # been visited.
        visitedHrefs.append(curPage)
        # Returns the BeautifulSoup of this page. An exception
        # is raised if parseSource tries to open a local file
        # that doesn't exist
        try:
            curSoup = parseSource(curPage)
        except IOError:
            continue
        # Checks the page for malware. If it finds some,
        # it prints out the URL of the page and the malware
        # that was found, and returns True.
        if malwares.findMalware(curSoup):
            print "Malware found on", curPage
            return True
        # Keeps track of the number of pages that have been scanned.
        # If the total reaches 26 or above, then we are stopping the
        # scan.
        numPages += 1
        if numPages > 25:
           print "Maximum number of pages reached" 
           break
        sys.stdout.write("\rDepth:{0}\tPage:{1}".format(curDepth, numPages))
        sys.stdout.flush()
        # Gets all the links on the page that point
        # to somewhere within the domain. It also checks to
        # see if external links in <script> and <img> tags
        # are flagged by google to be malicious.
        curHrefs = findPages(curSoup, domainUrl, curPage)
        if type(curHrefs) == tuple:
            print "Malware found on", curHrefs[0], "linked from", curPage, "inside a", curHrefs[1], "tag"
            return True
        # Checks to see if any of the found, valid links have
        # already been visited or found
        for href in curHrefs:
            if href not in visitedHrefs and href not in hrefQueue:
                hrefQueue.append(href)
                depthDict[href] = curDepth+1
    # If it gets through the loop, then there was no malware
    # to be found.
    print "\nNo malware found on this url!"
    return False

