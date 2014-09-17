Slack Utils
===========

A Python implementation of many Slack API functions designed to maximize ease-of-use.

Usage
=====

Installation
------------

Run `setup.py`.

Requirements
------------

* requests

Configuration
-------------

First of all, you'll need a [Slack](http://www.slack.com) account. The package can be installed in the standard fashion using `setup.py`. In order to use Slack's API, you'll need to generate an API token, which can be obtained from the [Slack API page](http://api.slack.com).

Basic Usage
-----------

Once installed, Slack can be used like this:

```python
from slackutils import Slack

s = Slack("YOUR-SLACK-TOKEN")

# Fetch channels, users, and groups.
s.channels()
s.users()
s.groups()

# Send a message to a user or a channel.
s.send(channel="channel", text="content")

# Upload or list files.
s.upload(filename="file.ext")
s.files(user="user")

# Interact with channels or groups.
s.history(channel="channel")
s.mark(channel="group")

# Search.
s.search(query="search", search_type="files")

# Make any other call to the API.
s.api(function="channels.join", data={"name": "channel"})
```

There are plenty of other options available for advanced usage, of course.

Sending a Message
-----------------

To send a message in Slack (probably the thing you'll want to do most often), use the `Slack` object's `send` function (which uses the Slack API's `chat.postMessage` function). But there are a few extra features.

If you want to send a message to a specific user or channel, you can prepend the exact destination name with either `@` or `#`. If you don't include either symbol, Slack Utils will search all users, channels, and private groups for a matching destination. The request may fail if multiple ambiguous destinations (or none) are found, so check the `Slack` object's `error` attribute. (If the object's `verbose` flag is set, you'll get suggestions for potential channel matches.)

If you call `send` with the `notify` flag, Slack Utils will parse the text looking for either `@username` or `@channel` (as appropriate); if the appropriate notification text is not found, it will be appended to the message to ensure that the user (or channel) in question will receive a notification.

Response
--------

Whenever a request is made to Slack's API, the full response (and any error that may have occurred) will be stored in the `response` and `error` elements of the `Slack` object. The full response will also be returned by the function.

If errors occurred, the `Slack` object's `error` attribute will contain a dictionary with the type of the error (`http` or `slack`) and the error code (e.g., `500` or `channel_not_found`). In the case of an HTTP error, the `Slack` object's `response` attribute will be empty; otherwise, it will contain the full response returned by Slack. To facilitate error-checking, the `Slack` object's `error` attribute is set to `None` when no errors are found.

### HTTP Error

```python
>>> s = Slack("YOUR-SLACK-TOKEN")
>>> s.response	# None
>>> s.error
{'code': 500, 'type': 'http'}
```

### Slack Error

```python
>>> s = Slack("YOUR-SLACK-TOKEN")
>>> s.send("somebody", "message")
{u'ok': True, u'ts': u'1410965023.000021', u'channel': u'D02549KAB'}
>>> s.send("nobody", "message")
{u'ok': False, u'error': u'channel_not_found'}
>>> s.error
{'code': u'channel_not_found', 'type': 'slack'}
```

Bugs and Feature Requests
=========================

Feature Requests
----------------

None

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

