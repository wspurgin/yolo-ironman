Yolo-Ironman
============

The Yolo-Ironman project is a python implemented web crawler & web scrapper.
<!-- view this file on the web here:
https://github.com/wspurgin/yolo-ironman/blob/master/README.md -->

Installation
------------

Dependencies and their installation instructions (or link to those instructions)
is included below this section.

### Using Git

You can clone this repository to gain access to the code of the project.

```
git clone https://github.com/wspurgin/yolo-ironman
```

### Downloading Tarball

Download the cutting edge latest version of Yolo-Ironman at
https://github.com/wspurgin/yolo-ironman/archive/master.zip

Dependencies
------------

### Python 2.7

Most operating systems come with Python installed out of the box. While most use
Python 2.7.x, your OS may not. If it does not have any Python, it is recommended
to [install Python 2.7](https://www.python.org/download/releases/2.7/).

### `requests` module

This project uses [Requests](http://docs.python-requests.org/en/latest/),
the "HTTP for Humans" python module. It is, like the claim suggests, a much
nicer HTTP implementation to use than the default python module. It can be
installed using `pip`.

```
pip install requests
```

You can also download the tarball, zipball, or use git following [these
instructions](http://docs.python-requests.org/en/latest/user/install/).

### `lxml`module

This project uses [lxml](https://pypi.python.org/pypi/lxml/2.3) as a pluggable
parser into `BeautifulSoup` (discussed below). It is a powerful (and wickedly
fast) XML parser. It can be installed using `pip`

```
pip install lxml
```

You can also install `lxml` natively on most Linux distributions or using  git
following [these instructions.](http://lxml.de/installation.html)

### `BeautifulSoup` module

This project also uses [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/). This can be easily utilized to look for
all of the links in any given webpage, and to extract all the text that is not
related to html tags. It can be installed using `pip`.

```
pip install beautifulsoup4
```

You can also download the tarball which can be found on the `BeautifulSoup`
documentation page.

Execution
---------

To execute the program, simply run jarvis.py inside of the scraper folder
with the python 2.7 interpreter.
```
~/yolo-ironman/scraper/$ python jarvis.py
```

###Command Line Arguments
There are a few arguments that can be passed:
1. A target URL to crawl
2. The limit on how many pages will be accessed
3. Words that should be ignored when indexing the pages

The first argument must either be a valid URL (including scheme), or the word
'none'
```
~/yolo-ironman/scraper/$ python jarvis.py http://lyle.smu.edu
~/yolo-ironman/scraper/$ python jarvis.py none
```

If 'none' is specified, then the default address of http://lyle.smu.edu/~fmoore
is crawled.

The second argument must either be a non-negative integer, or the word 'none'.
```
~/yolo-ironman/scraper/$ python jarvis.py http://lyle.smu.edu 20
~/yolo-ironman/scraper/$ python jarvis.py none none
```

Putting 1 will result in only the base URL being crawled (the first page), while
putting 'none' will put no limit on the number of pages to be crawled. This is
the default behavior, but it is necessary to put none if stop words need to be
included. Putting 0 will result in no pages being crawled.

The third argument accepts varying values as well. It can either be a path to a
txt file or a hand typed list of words on the command line
```
~/yolo-ironman/scraper/$ python jarvis.py http://google.com 20 stopwords.txt
~/yolo-ironman/scraper/$ python jarvis.py none 20 these are all my stop words
~/yolo-ironman/scraper/$ python jarvis.py none none stopwords.txt
```

The txt file MUST have words on separate lines:
```
These
Are
All
My
Stop
Words
```

Ironman Description
-------------------

### Directory Structure

The indexer, parser, crawler, runner, and all supporting code are located within
the `scraper` directory. The tests for each of the objects is under the `tests`
directory. This section of the documentation is specifically concerned with the
body of code under `scraper`. Below is summary information of certain classes
within the Yolo-Ironman project.

### Ironman

Ironman is the web-crawling, shiny-chrome-encased, proverbial workhorse of the
Yolo-Ironman project. It handles the fetching and crawling of a domain. In
general, these are the need to knows about Ironman:

#### Domain Exclusive

Ironman won't go cheating on other domains. You give Ironman a starting URL and
it'll stick to that starting URL's domain.

#### Observes Robots.txt

Hey, no hard feelings. Ironman knows that everybody has a few skeletons in the
closet. If you ask it not to go there, Ironman won't. It even <a
href="#user-content-robot">supports non-standard robot.txt locations!</a>

#### Politeness

Ironman is so polite, it won the peace prize at the bi-centennial Web Crawlers
of the World conference.

#### Supports Non-Standard Root Locations

If you've gone mad, and the world has run out of domains that you could possibly
call your own, fear not. Ironman hears you. You can use mom and dad's domain
with your subdirectory as the fake "root"/domain with Ironman.

```python
my_fake_domain = "http://mom_and_dads.domain.us/me"
yolo = Ironman(my_fake_domain, treat_as_root=True)
yolo.root
  #=> 'http://mom_and_dads.domain.us/me'
```

### 

### Robot

Robot (affectionately known as "Dummy" by Ironman) is a wrapper class around
python's `RobotFileParser` class to support non-standard locations of
`robots.txt` files.

For example:

```python
# robots.txt
# located at: http://lyle.smu.edu/~wspurgin/robots.txt
# User-agent: *
# Disallow: /dontgohere/

# RobotFileParser from robotparser
r = RobotFileParser()
r.set_url("http://lyle.smu.edu/~wspurgin/robots.txt")
r.read()

# ✗ This result was not intended by the creator of the robots.txt
r.can_fetch("http://lyle.smu.edu/~wspurgin/dontgohere/")
#  => True

# Using Robot
robot = Robot()
robot.set_url("http://lyle.smu.edu/~wspurgin/robots.txt")
robot.read()

# ✓ This produces the result intended by the creator of the robots.txt
robot.can_fetch("http://lyle.smu.edu/~wspurgin/dontgohere/")
#  => False
```

### Crawl

Crawl, apart from being rather poorly named, is nothing noteworthy. It simply
holds results from a single crawl that Ironman does and makes them nice and
printable.

### Jarvis

What would Ironman be without Jarvis? Just an awesome, fully functioning, shiny
web-crawler-to-beat-all-web-crawlers! True. However, sometimes you just need a
to have a good crawl and don't want to bother with writing a script and dealing
with this output or reading through that class's docs. We get it. Jarvis is a
handy-dandy command line program for just having a crawl. It'll crawl
http://lyle.smu.edu/~fmoore by default and print out some nice summary things
for you. However you can give it all kinds of <a
href="#user-content-command-line-arguments">command line arguemnts</a>!
Consider it an inspiration for when you want to write your own crawl.  :wink:
