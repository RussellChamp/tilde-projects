#!/usr/bin/python3

import datetime
import fileinput
import time
import calendar
import re
import operator
from util import nameFix

MAX_NODES = 5

logfile = "/home/archangelic/irc/log"
timeCutoff = calendar.timegm(time.gmtime()) - (3 * 7 * 24 * 60 * 60)  # 3 weeks

def whoSaid(text):
    if not text:
        return "No text given :("
    else:
        result = whoSaid_data(text)
        date = datetime.date.fromtimestamp(result["timecutoff"])
        dateStr = date.strftime("%B %d")
        if not result["data"]:
            msg = "Nobody said '%s' since %s" % (text, dateStr)
        else:
            msg = "Since %s, %s said '%s' %d times" % (
                dateStr,
                result["data"][0][0],
                text,
                result["data"][0][1],
            )
            if len(result["data"]) > 1:
                msg += " and %s said it %d times" % (
                    result["data"][1][0],
                    result["data"][1][1],
                )
        return msg

def whoSaid_data(word):
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
                user = nameFix.fixName(user).lower()
            except ValueError:
                continue  # There are some bad lines in the log file that we'll ignore if we can't parse

            if time > timeCutoff and message[0] is not "!" and word in message.lower():
                if user in userData:
                    userData[user] += 1
                else:
                    userData[user] = 1
    userData = sorted(userData.items(), key=operator.itemgetter(1), reverse=True)
    return {"timecutoff": timeCutoff, "data": userData}

