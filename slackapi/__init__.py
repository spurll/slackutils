# Written by Gem Newman. This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 3.0 Unported License.


import requests, re


class Slack():
    def __init__(self, token, name=None, icon=None, verbose=False):
        self.token = token
        self.name = name
        self.icon = icon
        self.verbose = verbose
        self.user_list = None
        self.channel_list = None


    def send(self, target, message, name=None, icon=None, link_names=True,
             notify=False):
        """
        Sends a message using Slack.
        """

        target = self.destination(target)

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
        r = requests.post("https://slack.com/api/chat.postMessage",
                          data=payload)

        if check_response(r) and self.verbose:
            print "Message delivered to {}.".format(target["name"])


    def users(self, refresh=False):
        """
        Retrieves (and caches) all available Slack users.
        """

        if refresh or not self.user_list:
            p = {"token": self.token}
            r = requests.post("https://slack.com/api/users.list", data=p)

            if check_response(r):
                self.user_list = r.json()["members"]

        return self.user_list


    def channels(self, refresh=False):
        """
        Retrieves (and caches) all available Slack channels.
        """

        if refresh or not self.channel_list:
            p = {"token": self.token, "exclude_archived": 1}
            r = requests.post("https://slack.com/api/channels.list", data=p)

            if check_response(r):
                self.channel_list = r.json()["channels"]

        return self.channel_list


    def upload(self, filename, filetype=None, title=None, comment=None,
               target=None):
        """
        Uploads a file to Slack. If posting the file to one or more channels,
        the target argument can be either a single channel or a list.
        """

        if type(target) is list:
            target = ", ".join(self.destination(t)["id"] for t in target)
        elif target:
            target = self.destination(target)["id"]

        files = {'file': open(filename, 'rb')}
        payload = {"token": self.token,
                   "filename": filename,
                   "filetype": filetype,
                   "title": title,
                   "initial_comment": comment,
                   "channels": target}
        r = requests.post("https://slack.com/api/files.upload", data=payload,
                          files=files)

        if check_response(r) and self.verbose:
            print "File uploaded successfully."


    def history(self, channel, latest=None, oldest=None, count=None):
        pass


    def mark(self, channel, time=None):
        pass


    def files(self, channel, user=None, start_time=None, end_time=None,
              types=None, count=None, page=None):
        pass


    def search(self, query, sort=None, sort_direction=None, highlight=None,
               count=None, page=None):
        pass


    def destination(self, target):
        """
        Takes a partial or inexact destination and finds the best match from
        among the available channels and users.
        """

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

        if not found:
            raise Exception('No users or channels named "{}".'.format(target))
        else:
            raise Exception('Unable to identify destination. Possible matches:'
                            ' {}'.format(', '.join(i["name"] for i in found)))


def check_response(r):
    # Check the HTTP response.
    if r.status_code != 200:
        raise Exception("HTTP request returned {}: {}."
                        .format(r.status_code, r.text))

    # Request was successful. Now check Slack's response.
    if not r.json()["ok"]:
        raise Exception('Slack API returned "{}".'.format(r.json()["error"]))

    return True

