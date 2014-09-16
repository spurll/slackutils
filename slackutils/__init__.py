# Written by Gem Newman. This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.


import requests, re, datetime, time


URL = "https://slack.com/api/"


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

        # Test authentication on startup.
        self.test()


    def test(self):
        """
        Tests authentication.
        """

        payload = {"token": self.token}
        self.parse(requests.post(URL + "auth.test", data=payload))

        if self.verbose and not self.error:
            print "Authenticated as {} of {}.".format(self.response["user"],
                                                      self.response["team"])


    def send(self, channel, message, name=None, icon=None, link_names=True,
             notify=False):
        """
        Sends a message using Slack.
        """

        target = self.destination(channel)

        if target and notify:
            if target[0] == "@" and target not in message:
                message += ("\n" if "\n" in message else " ") + target
            elif target[0] == "#" and "@channel" not in message:
                message += ("\n" if "\n" in message else " ") + "@channel"

        payload = {"token": self.token,
                   "channel": target["id"] if type(target) == dict else target,
                   "username": name if name else self.name,
                   "icon_url": icon if icon else self.icon,
                   "link_names": int(link_names),
                   "text": message}
        self.parse(requests.post(URL + "chat.postMessage", data=payload))

        if self.verbose and not self.error:
            print "Message delivered to {}.".format(target["name"])

        return self.response


    def users(self):
        """
        Retrieves (and caches) all available Slack users.
        """

        payload = {"token": self.token}
        self.parse(requests.post(URL + "users.list", data=payload))

        if not self.error:
            self.user_list = self.response["members"]

        return self.response


    def channels(self, exclude_archived=True):
        """
        Retrieves (and caches) all available Slack channels.
        """

        payload = {"token": self.token,
                   "exclude_archived": bool(exclude_archived)}
        self.parse(requests.post(URL + "channels.list", data=payload))

        if not self.error:
            self.channel_list = self.response["channels"]

        return self.response


    def upload(self, filename, filetype=None, title=None, comment=None,
               target=None):
        """
        Uploads a file to Slack. If posting the file to one or more channels,
        the target argument can be either a single channel or a list.
        """

        if type(target) is list:
            target = ",".join(self.destination(t).get("id") for t in target)
        elif target:
            target = self.destination(target).get("id")
        if not target: return None

        files = {'file': open(filename, 'rb')}
        payload = {"token": self.token,
                   "filename": filename,
                   "filetype": filetype,
                   "title": title,
                   "initial_comment": comment,
                   "channels": target}
        self.parse(requests.post(URL+"files.upload",data=payload,files=files))

        if self.verbose and not self.error:
            print "File uploaded successfully."

        return self.response


    def history(self, channel, latest=None, oldest=None, count=None):
        """
        Checks a channel's message history.
        """
        target = self.destination(channel)
        if not target: return None

        if type(oldest) == datetime.date or type(oldest) == datetime.datetime:
            oldest = time.mktime(oldest.timetuple())

        if type(latest) == datetime.date or type(latest) == datetime.datetime:
            latest = time.mktime(latest.timetuple())

        payload = {"token": self.token,
                   "channel": target["id"] if type(target) == dict else target,
                   "latest": latest,
                   "oldest": oldest,
                   "count": count}
        self.parse(requests.post(URL + "channels.history", data=payload))

        if self.verbose and not self.error:
            print "Fetched history for channel {}.".format(target["name"]
                  if type(target) == dict else target)

        return self.response


    def mark(self, channel, ts=datetime.datetime.now()):
        """
        Sets the channel's "read" marker to a specific time.
        """
        target = self.destination(channel)
        if not target: return None

        if type(ts) == datetime.date or type(ts) == datetime.datetime:
            ts = time.mktime(ts.timetuple())

        payload = {"token": self.token,
                   "channel": target["id"] if type(target) == dict else target,
                   "ts": ts}
        self.parse(requests.post(URL + "channels.mark", data=payload))

        if self.verbose and not self.error:
            print "Marked channel {} as read.".format(target["name"])

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

        payload = {"token": self.token,
                   "user": target["id"] if type(target) == dict else None,
                   "ts_to": latest,
                   "ts_from": oldest,
                   "types": types,
                   "count": count,
                   "page": page}
        self.parse(requests.post(URL + "files.list", data=payload))

        if self.verbose and not self.error:
            print "Fetched file list."

        return self.response


    def search(self, query, sort=None, sort_direction=None, highlight=None,
               count=None, page=None, search_type="all"):
        pass


    def destination(self, target, refresh=False):
        """
        Takes a partial or inexact destination and finds the best match from
        among the available channels and users. Channel names prepended with 
        """

        if not target:
            return target

        # Refresh lists of users and channels if necessary.
        if refresh or not self.user_list: self.users()
        if refresh or not self.channel_list: self.channels()

        if target[0] == "@":
            # Exact match for a user.
            found = [u for u in self.user_list if u["name"] == target[1:]]

        elif target[0] == "#":
            # Exact match for a channel.
            found = [c for c in self.channel_list if c["name"] == target[1:]]

        else:
            # Inexact match.
            found = [i for i in self.channel_list + self.user_list
                     if target.lower() in i["name"].lower() or ("real_name" in
                     i and target.lower() in i["real_name"].lower())]

        if len(found) == 1:
            return found[0]

        if self.verbose:
            if not found:
                print 'No users or channels found named "{}".'.format(target)
            else:
                print 'Unable to identify destination. Possible matches: {}'  \
                      .format(', '.join(i["name"] for i in found))

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
            print "Error: {}".format(self.error)
