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

After which you may run the crawler with TODO

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
