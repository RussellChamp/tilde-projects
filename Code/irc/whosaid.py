#!/usr/bin/python
import fileinput
import time
import calendar
import re
import operator

MAX_NODES = 5

logfile = "/home/jumblesale/Code/irc/log"
timeCutoff = calendar.timegm(time.gmtime()) - (3 * 7 * 24 * 60 * 60)  # 3 weeks

nameFix = {
    "jumblesal": "jumblesale",
    "hardmath1": "kc",
    "hardmath123": "kc",
    "bendorphan": "endorphant",
    "endorphan": "endorphant",
    "synergian": "synergiance",
}


def whoSaid(word):
    word = word.lower()
    userData = (
        {}
    )  # hash keyed by "user" that contains a hash of mentioned other users with count
    # Get a list of all user names by checking the logs for people who have said things
    with open(logfile, "r") as log:
        for line in log:
            try:
                time, user, message = line.split("\t", 3)
                time = int(time)
                if nameFix.has_key(user):
                    user = nameFix[user]
                else:
                    user = user.lower()
            except ValueError:
                continue  # There are some bad lines in the log file that we'll ignore if we can't parse

            if time > timeCutoff and message[0] is not "!" and word in message.lower():
                if user in userData:
                    userData[user] += 1
                else:
                    userData[user] = 1
    userData = sorted(userData.items(), key=operator.itemgetter(1), reverse=True)
    return {"timecutoff": timeCutoff, "data": userData}
