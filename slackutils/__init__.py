# Written by Gem Newman. This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.


import requests, re, datetime, time, json


API_URL = "https://slack.com/api/"


class Slack():
    def __init__(self, token, name=None, icon=None, error=True, verbose=False):
        # Settings
        self.token = token
        self.name = name
        self.icon = icon
        self.verbose = verbose

        # Response from Slack
        self.response = None
        self.error = None

        # Cache
        self.user_list = []
        self.channel_list = []
        self.group_list = []

        # Test authentication on startup.
        self.test()


    def api(self, function, data=dict()):
        """
        Provides basic API functionality.
        """

        if "token" not in data: data["token"] = self.token
        self.parse(requests.post(API_URL + function, data=data))
        return self.response


    def test(self):
        """
        Tests authentication.
        """

        self.api("auth.test")

        if self.verbose and not self.error:
            print("Authenticated as {} of {}.".format(self.response["user"],
                                                      self.response["team"]))


    def send(self, channel, text, name=None, icon=None, link_names=True,
             parse=None, attachments=None, unfurl_links=False, icon_emoji=None,
             notify=False):
        """
        Sends a message using Slack.
        """

        target = self.destination(channel)

        if notify and type(target) is dict:
            n = "@channel" if target.get("is_channel") or                     \
                              target.get("is_group") else "@"+target["name"]
            if n not in text:
                text += ("\n" if "\n" in text else " ") + n

        payload = {"channel": target["id"] if type(target) is dict else target,
                   "username": name if name else self.name,
                   "parse": parse,
                   "icon_url": icon if icon else self.icon,
                   "attachments": json.dumps(attachments),
                   "icon_emoji": icon_emoji,
                   "link_names": int(link_names),
                   "unfurl_links": int(unfurl_links),
                   "text": text}
        self.api("chat.postMessage", payload)

        if self.verbose and not self.error:
            print("Message delivered to {}.".format(target["name"]
                  if type(target) is dict else target))

        return self.response


    def users(self):
        """
        Retrieves (and caches) all available Slack users.
        """

        self.api("users.list")

        if not self.error:
            self.user_list = self.response["members"]

        return self.response


    def channels(self, exclude_archived=True):
        """
        Retrieves (and caches) all available Slack channels.
        """

        self.api("channels.list", {"exclude_archived": int(exclude_archived)})

        if not self.error:
            self.channel_list = self.response["channels"]

        return self.response


    def groups(self, exclude_archived=True):
        """
        Retrieves (and caches) all available private Slack groups.
        """

        self.api("groups.list", {"exclude_archived": int(exclude_archived)})

        if not self.error:
            self.group_list = self.response["groups"]

        return self.response


    def upload(self, filename, filetype=None, title=None, comment=None,
               channels=None):
        """
        Uploads a file to Slack. If posting the file to one or more channels,
        the target argument can be either a single channel or a list.
        """

        if type(channels) is list:
            target = [self.destination(c) for c in channels]
            target = ",".join(c["id"] if type(c) is dict else c
                              for c in target)
        elif channels:
            target = self.destination(channels)
            if type(target) == "dict": target = target["id"]
        else:
            target = None

        with open(filename, "rb") as data:
            payload = {"content": data.read(),
                       "filename": filename,
                       "filetype": filetype,
                       "title": title,
                       "initial_comment": comment,
                       "channels": target}
        self.api("files.upload", payload)

        if self.verbose and not self.error:
            print("File uploaded successfully.")

        return self.response


    def history(self, channel, latest=None, oldest=None, count=None,
                target_type=None):
        """
        Checks a channel or group's message history.
        """

        target = self.destination(channel)

        if not target_type:
            target_type = "groups" if type(target) is dict and                \
                                      target.get("is_group") else "channels"

        if type(oldest) == datetime.date or type(oldest) == datetime.datetime:
            oldest = time.mktime(oldest.timetuple())

        if type(latest) == datetime.date or type(latest) == datetime.datetime:
            latest = time.mktime(latest.timetuple())

        payload = {"channel": target["id"] if type(target) is dict else target,
                   "latest": latest,
                   "oldest": oldest,
                   "count": count}
        self.api(target_type + ".history", payload)

        if self.verbose and not self.error:
            print("Fetched history for {}.".format(target["name"] if
                  type(target) is dict else target))

        return self.response


    def mark(self, channel, ts=datetime.datetime.now(), target_type=None):
        """
        Sets a channel or group's "read" marker to a specific time.
        """

        target = self.destination(channel)

        if not target_type:
            target_type = "groups" if target in self.group_list else "channels"

        if type(ts) == datetime.date or type(ts) == datetime.datetime:
            ts = time.mktime(ts.timetuple())

        payload = {"channel": target["id"] if type(target) is dict else target,
                   "ts": ts}
        self.api(target_type + ".mark", payload)

        if self.verbose and not self.error:
            print("Marked {} as read.".format(target["name"]))

        return self.response


    def files(self, user=None, oldest=None, latest=None, types=None,
              count=None, page=None):
        """
        Lists all files available to the user.
        """

        target = self.destination(user)

        if type(oldest) == datetime.date or type(oldest) == datetime.datetime:
            oldest = time.mktime(oldest.timetuple())

        if type(latest) == datetime.date or type(latest) == datetime.datetime:
            latest = time.mktime(latest.timetuple())

        if type(types) is list:
            types = ",".join(types)

        payload = {"user": target["id"] if type(target) is dict else None,
                   "ts_to": latest,
                   "ts_from": oldest,
                   "types": types,
                   "count": count,
                   "page": page}
        self.api("files.list", payload)

        if self.verbose and not self.error:
            print("Fetched file list.")

        return self.response


    def search(self, query, sort=None, search_type="all", sort_direction=None,
               highlight=False, count=None, page=None):
        """
        Searches either files, messages, or both (the default).
        """

        payload = {"query": query,
                   "sort": sort,
                   "sort_dir": sort_direction,
                   "highlight": int(highlight),
                   "count": count,
                   "page": page}
        self.api("search" + search_type, payload)

        if self.verbose and not self.error:
            print('Searched {} for "{}".'.format(search_type, query))

        return self.response


    def destination(self, target, refresh=False):
        """
        Takes a partial or inexact destination and finds the best match from
        among the available users, channels, and groups. Channel names
        prepended with "#" and user names prepended with "@" indicate an exact
        match; all other destinations take "fuzzy" matches.
        """

        # Either nothing to find or it's already a fully-qualified destination.
        if not target or type(target) is dict:
            return target

        # Refresh lists of users and channels if necessary.
        if refresh or not self.user_list: self.users()
        if refresh or not self.channel_list: self.channels()
        if refresh or not self.group_list: self.groups()

        if target[0] == "@":
            # Exact match for a user.
            found = [u for u in self.user_list if u["name"] == target[1:]]

        elif target[0] == "#":
            # Exact match for a channel.
            found = [c for c in self.channel_list if c["name"] == target[1:]]

        else:
            # Inexact match.
            found = [i for i in self.channel_list + self.user_list +
                     self.group_list if target.lower() in i["name"].lower() or
                     ("real_name" in i and target.lower() in
                     i["real_name"].lower())]

        if len(found) == 1:
            return found[0]

        if self.verbose:
            if not found:
                print('Unable to find any users, channels, or groups named '
                      '"{}".'.format(target))
            else:
                print('Unable to identify destination. Possible matches: {}'
                      .format(', '.join(i["name"] for i in found)))

        return target


    def parse(self, response):
        """
        Receives a response from a request to the Slack API, parses it for
        errors, and stores the results in self.response and self.error.
        """

        # Check the HTTP response.
        if response.status_code != 200:
            self.error = {"type": "http", "code": response.status_code}
            self.response = None

        else:
            # HTTP request was successful. Now check Slack's response.
            self.response = response.json()
            if not self.response["ok"]:
                self.error = {"type": "slack", "code": self.response["error"]}
            else:
                self.error = None

        if self.error and self.verbose:
            print("Error: {}".format(self.error))
