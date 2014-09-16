Slack Utils
===========

A Python implementation of many Slack API functions designed to maximize ease-of-use.

Installation
============

Configuration
-------------

First of all, you'll need a [Slack](http://www.slack.com) account. The package can be installed in the standard fashion using `setup.py`. In order to use Slack's API, you'll need to generate an API token, which can be obtained from the [Slack API page](http://api.slack.com).

Once installed, Slack can be used like this:

```python
from slackutils import Slack

s = Slack("your-slack-token")
s.send(target="channel", message="content")
s.upload(filename="file")
s.files(user="user")
s.history(channel="channel")
s.mark(channel="channel")
```

There are plenty of other options available for advanced usage, of course.

Requirements
------------

* requests

Bugs and Feature Requests
=========================

Feature Requests
----------------

Not yet implemented:

* `auth.test`
* `chat.postMessage` (`Slack.send` doesn't support all API features yet)
* `search.files`
* `search.messages`
* `search.all`

Other requested changes:

* It would be good to have a generic API calling function that takes a function name (e.g., `files.info`) and a dictionary of arguments, adds the auth token and passes it along.
* The fuzzy-match `destination` function just prints stuff when it encounters an error. If `verbose` is set, that's fine, but it really should return this value in some way. You know, being an API implementation and all.

Known Bugs
----------

None

Slack
=====

Information about Slack is available on [their website](http://www.slack.com). Information about the Slack API is available [here](http://api.slack.com).

A Note on Slacker
=================

There is at least one other Slack API implementation out there on PyPI. [Slacker](https://pypi.python.org/pypi/slacker/0.3.3) is a full-feature implementation of Slack's API and does exactly what it says on the tin. Slack's API is powerful, but pretty raw. It's my intention to make this Slack Utils a little easier to work with (with fuzzy destination matching, handling datetimes and lists, and the like). Slacker may be more in line with what you're looking for, so you should to check it out.

License Information
===================

Written by Gem Newman. [GitHub](https://github.com/spurll/) | [Blog](http://www.startleddisbelief.com) | [Twitter](https://twitter.com/spurll)

This work is licensed under Creative Commons [BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/).

