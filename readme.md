Slack Utils
===========

A Python implementation of many Slack API functions designed to maximize ease-of-use.

Usage
=====

Configuration
-------------

First of all, you'll need a [Slack](http://www.slack.com) account. The package can be installed in the standard fashion using `setup.py`. In order to use Slack's API, you'll need to generate an API token, which can be obtained from the [Slack API page](http://api.slack.com).

Usage
-----

Once installed, Slack can be used like this:

```python
from slackutils import Slack

s = Slack("your-slack-token")
s.send(target="channel", message="content")
s.channels()
s.users()
s.upload(filename="file")
s.files(user="user")
s.history(channel="channel")
s.mark(channel="channel")
```

There are plenty of other options available for advanced usage, of course.

Response
--------

Whenever a request is made to Slack's API, the full response (and any error that may have occurred) will be stored in the `response` and `error` elements of the `Slack` object. The full response will also be returned by the function.

If errors occurred, `s.error` will contain a dictionary with the type of the error (`http` or `slack`) and the error code (e.g., `400` or `channel_not_found`). In the case of an HTTP error, `s.response` will be empty; otherwise, it will contain the full response returned by Slack. To facilitate error-checking, `s.error` is set to `None` when no errors are found.

Requirements
------------

* requests

Bugs and Feature Requests
=========================

Feature Requests
----------------

Not yet implemented:

* `chat.postMessage` (`Slack.send` doesn't support all API features yet)
* `search.files`
* `search.messages`
* `search.all`
* `groups.history`
* `groups.list`
* `groups.mark`

Other requested changes:

* `send` (and `destination`) don't support private groups yet.
* It would be good to have a generic API calling function that takes a function name (e.g., `files.info`) and a dictionary of arguments, adds the auth token and passes it along.

Known Bugs
----------

None

Slack
=====

Information about Slack is available on [their website](http://www.slack.com). Information about the Slack API is available [here](http://api.slack.com).

A Note on Slacker
=================

There is at least one other Slack API implementation out there on PyPI. [Slacker](https://pypi.python.org/pypi/slacker/0.3.3) is a full-feature implementation of Slack's API and does exactly what it says on the tin. Slack's API is powerful, but pretty raw. It's my intention to make SlackUtils a little easier to work with (with fuzzy destination matching, handling datetimes and lists, and the like). Slacker may be more in line with what you're looking for, so you should to check it out.

License Information
===================

Written by Gem Newman. [GitHub](https://github.com/spurll/) | [Blog](http://www.startleddisbelief.com) | [Twitter](https://twitter.com/spurll)

This work is licensed under Creative Commons [BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/).

