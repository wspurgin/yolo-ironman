Yolo-Ironman
============

The Yolo-Ironman project is a python implemented web crawler & web scrapper.

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

### 'BeautifulSoup' module

This project also uses [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/). This can be easily utilized to look for
all of the links in any given webpage, and to extract all the text that is not
related to html tags. It can be installed using `pip`.

```
pip install beautifulsoup4
```

You can also download the tarball which can be found on the BeautifulSoup
documentation page.

### TODO Any further dependencies

## Ironman Description and Specification

### Robot

- The wrapper class around python's `RobotFileParser` class that supports
  non-standard locations of `robots.txt` files.
- An example:

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

Execution
---------

To execute the program, simply run jarvis.py inside of the scraper folder
with the python 2.7 interpreter.
```
~/yolo-ironman/scraper/$ python jarvis.py
```

###Command Line Arguments
There are a few arguments that can be passed:
1. The limit on how many pages will be accessed
2. Words that should be ignored when indexing the pages

The first argument must either be a non-negative integer, or the word 'none'.
```
~/yolo-ironman/scraper/$ python jarvis.py 20
~/yolo-ironman/scraper/$ python jarvis.py none
```

Putting 1 will result in only the base URL being crawled (the first page), while
putting 'none' will put no limit on the number of pages to be crawled. This is the
default behavior, but it is necessary to put none if stop words need to be 
included. Putting 0 will result in no pages being crawled. 

The second argument accepts varying values as well. It can either be a path to a txt
file or a hand typed list of words on the command line
```
~/yolo-ironman/scraper/$ python jarvis.py 20 stopwords.txt
~/yolo-ironman/scraper/$ python jarvis.py 20 these are all my stop words
~/yolo-ironman/scraper/$ python jarvis.py none stopwords.txt
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
