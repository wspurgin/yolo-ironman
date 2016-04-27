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

This project also uses
[BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/bs4/doc/). This can
be easily utilized to look for all of the links in any given webpage, and to
extract all the text that is not related to html tags. It can be installed using
`pip`.

```
pip install beautifulsoup4
```

You can also download the tarball which can be found on the [BeautifulSoup
documentation page](http://www.crummy.com/software/BeautifulSoup/bs4/doc/).

Execution
---------

To execute the program, simply run the yolo executable in the exe folder.
On ubuntu and mac: 
```
~/yolo-ironman/exe$ ./yolo
```

We have not tested windows, but maybe you can double click it? We're not sure.
Perhaps you can also run it using the CLI for windows as long as you have all
the packages install.

###Command Line Arguments
There are no true command line arguments when running the program. However, we
have created an interface that resembles the CLI. After executing the yolo file,
your console will look like this:
```
~/yolo-ironman/exe$ ./yolo
>
```
Once the > shows up, the program is ready to accept commands. There are 6 total
commands (Note: These ARE case-sensitive):
1. buildIndex [url]- Builds the index from a specified URL. If none is supplied, it defaults to http://lyle.smu.edu/~fmoore/
2. query all_query_words - Can only be executed after buildIndex. 
    all_query_words is all of the words that want to be queried separated by a space.
    ```
    >query find all these words
    ```
3. quit - Exits the program
4. loadStopWords path/to/file - Loads in a file that contains stopwords separated by newline. A stopword list is supplied by default.
5. setK positive_integer - Sets the value of K, which determines the most amount of documents returned for a query
6. help [command] - By default lists all the commands available, or if a command is supplied, returns the docstring for that command.

Ironman Description
-------------------

### Directory Structure

The indexer, parser, crawler, runner, query engine, UI, and all supporting code 
are located within the `scraper` directory. The tests for each of the objects is
under the `tests` directory. This section of the documentation is specifically
concerned with the body of code under `scraper`. Below is summary information of 
certain classes within the Yolo-Ironman project.

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
web-crawler-to-beat-all-web-crawlers! Jarvis handles the interaction between the
UI and the crawler. 

### Pepper

Tony Stark's image would be nothing without Pepper Pots. She is the query handler.
Everytime you use the query command, Pepper takes care of it. No bones about it.