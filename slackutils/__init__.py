# Written by Gem Newman. This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.


import requests, re, datetime, time


class Slack():
    def __init__(self, token, name=None, icon=None, error=True, verbose=False):
        self.token = token
        self.name = name
        self.icon = icon
        self.verbose = verbose
        self.response = None
        self.user_list = None
        self.channel_list = None


    def send(self, target, message, name=None, icon=None, link_names=True,
             notify=False):
        """
        Sends a message using Slack.
        """

        target = self.destination(target)
        if not target: return None

        if notify:
            if target[0] == "@" and target not in message:
                message += ("\n" if "\n" in message else " ") + target
            elif target[0] == "#" and "@channel" not in message:
                message += ("\n" if "\n" in message else " ") + "@channel"

        payload = {"token": self.token,
                   "channel": target["id"],
                   "username": name if name else self.name,
                   "icon_url": icon if icon else self.icon,
                   "link_names": int(link_names),
                   "text": message}
        self.response = requests.post("https://slack.com/api/chat.postMessage",
                                      data=payload)

        e = self.check_errors()
        if self.verbose:
            if e:
                print "Slack returned the following error: {}".format(e)
            else:
                print "Message delivered to {}.".format(target["name"])


    def users(self, refresh=False):
        """
        Retrieves (and caches) all available Slack users.
        """

        if refresh or not self.user_list:
            payload = {"token": self.token}
            self.response = requests.post("https://slack.com/api/users.list",
                                          data=payload)

            e = self.check_errors()
            if e:
                if self.verbose:
                    print "Slack returned the following error: {}".format(e)
            else:
                self.user_list = self.response.json()["members"]

        return self.user_list


    def channels(self, refresh=False):
        """
        Retrieves (and caches) all available Slack channels.
        """

        if refresh or not self.channel_list:
            payload = {"token": self.token, "exclude_archived": 1}
            self.response = requests.post("https://slack.com/api/channels."
                                          "list", data=payload)

            e = self.check_errors()
            if e:
                if self.verbose:
                    print "Slack returned the following error: {}".format(e)
            else:
                self.channel_list = self.response.json()["channels"]

        return self.channel_list


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
        self.response = requests.post("https://slack.com/api/files.upload",
                                      data=payload, files=files)

        e = self.check_errors()
        if self.verbose:
            if e:
                print "Slack returned the following error: {}".format(e)
            else:
                print "File uploaded successfully."


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
                   "channel": target["id"],
                   "latest": latest,
                   "oldest": oldest,
                   "count": count}
        self.response = requests.post("https://slack.com/api/channels.history",
                                      data=payload)

        e = self.check_errors()
        if self.verbose:
            if e:
                print "Slack returned the following error: {}".format(e)
            else:
                print "Fetched history for channel {}.".format(target["name"])

        return self.response.json().get("messages")


    def mark(self, channel, ts=datetime.datetime.now()):
        """
        Sets the channel's "read" marker to a specific time.
        """
        target = self.destination(channel)
        if not target: return None

        if type(ts) == datetime.date or type(ts) == datetime.datetime:
            ts = time.mktime(ts.timetuple())

        payload = {"token": self.token,
                   "channel": target["id"],
                   "ts": ts}
        self.response = requests.post("https://slack.com/api/channels.mark",
                                      data=payload)

        e = self.check_errors()
        if self.verbose:
            if e:
                print "Slack returned the following error: {}".format(e)
            else:
                print "Marked channel {} as read.".format(target["name"])


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
                   "user": target["id"] if target else None,
                   "ts_to": latest,
                   "ts_from": oldest,
                   "types": types,
                   "count": count,
                   "page": page}
        self.response = requests.post("https://slack.com/api/files.list",
                                      data=payload)

        e = self.check_errors()
        if self.verbose:
            if e:
                print "Slack returned the following error: {}".format(e)
            else:
                print "Fetched file list."

        return self.response.json().get("files")


    def search(self, query, sort=None, sort_direction=None, highlight=None,
               count=None, page=None, search_type="all"):
        pass


    def destination(self, target):
        """
        Takes a partial or inexact destination and finds the best match from
        among the available channels and users.
        """

        if not target:
            return target

        if target[0] == "@":
            # Exact match for a user.
            found = [u for u in self.users() if u["name"] == target[1:]]

        elif target[0] == "#":
            # Exact match for a channel.
            found = [c for c in self.channels() if c["name"] == target[1:]]

        else:
            # Inexact match.
            found = [i for i in self.channels() + self.users()
                     if target.lower() in i["name"].lower() or ("real_name" in
                     i and target.lower() in i["real_name"].lower())]

        if len(found) == 1:
            return found[0]


        # SHOULDN'T HAVE PRINT STATEMENTS HERE. SHOULD RETURN SOMETHING
        # INSTEAD?  


        if not found:
            print 'No users or channels named "{}".'.format(target)
        else:
            print 'Unable to identify destination. Possible matches: {}'      \
                  .format(', '.join(i["name"] for i in found))
        return None


    def check_errors(self):
        # Check the HTTP response.
        if self.response.status_code != 200:
            raise Exception("HTTP request returned {}: {}.".format(
                            self.response.status_code, self.response.text))

        # Request was successful. Now check Slack's response.
        r = self.response.json()
        if not r["ok"]:
            return r["error"]

        return False

