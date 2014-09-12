Slack API
=========

A (fairly) complete implementation of the Slack API.

Installation
============

Configuration
-------------

First of all, you'll need a [Slack](http://www.slack.com) account. The package can be installed in the standard fashion using `setup.py`. In order to use Slack's API, you'll need to generate an API token, which can be obtained from the [Slack API page](http://api.slack.com)).

Once installed, the Slack API can be used like this:

```python
from slackapi import Slack

s = Slack("your-slack-token")
s.send(target="channel", message="content")
s.upload(filename="file")
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

* `channels.history`
* `channels.mark`
* `files.list`
* `search.all`

Known Bugs
----------

None

Slack
=====

Information about Slack is available on [their website](http://www.slack.com). Information about the Slack API is available [here](http://api.slack.com).

A Note on Slacker
=================

There is at least one other Slack API implementation out there on PyPI. It's called [Slacker](https://pypi.python.org/pypi/slacker/0.3.3), and it's apparently a full-feature implementation (I haven't looked into it). It may be more in line with what you're looking for, so you may want to check it out.

License Information
===================

Written by Gem Newman. [GitHub](https://github.com/spurll/) | [Blog](http://www.startleddisbelief.com) | [Twitter](https://twitter.com/spurll)

This work is licensed under Creative Commons [BY-NC-SA 3.0](https://creativecommons.org/licenses/by-nc-sa/3.0/).

