#!/usr/bin/python
import fileinput
import json
import time
import calendar
import shutil
import re
import math
import operator

MAX_NODES = 4

logfile = "/home/archangelic/irc/log"
# logfile = "/home/jumblesale/Code/irc/log"
outfile = "/home/krowbar/logs/chatBesties.json"
outCircle = "/home/krowbar/logs/chatcircle.json"
timePeriod = calendar.timegm(time.gmtime()) - (2 * 7 * 24 * 60 * 60)  # 2 weeks

# hash keyed by "user" that contains a hash of mentioned other users with count
userData = {}
nameFix = {
    "jumblesal": "jumblesale",
    "hardmath1": "kc",
    "hardmath123": "kc",
    "bendorphan": "endorphant",
    "endorphan": "endorphant",
    "synergian": "synergiance",
}

users = []
# Get a list of all user names by checking the logs for people who have said things
with open(logfile, "r") as log:
    for line in log:
        try:
            time, user, message = line.split("\t", 3)
            if int(time) < timePeriod:
                continue  # only add users who have spoken in the last period
            if nameFix.has_key(user):
                user = nameFix[user]
            else:
                user = user.lower()

            if user not in users:
                users.append(user)
        except ValueError:
            continue  # There are some bad lines in the log file that we'll ignore if we can't parse

d3data = {}
d3data["nodes"] = []

# re-read the log and this time look for instances of user names in messages
with open(logfile, "r") as log:
    for line in log:
        try:
            time, user, message = line.split("\t", 3)
            if int(time) < timePeriod:
                continue  # only consider the past three weeks of chats
            if nameFix.has_key(user):
                user = nameFix[user]
            else:
                user = user.lower()
        except ValueError:
            continue  # There are some bad lines in the log file that we'll ignore if we can't parse
        for word in message.split(" "):
            word = re.sub("[^A-Za-z0-9]+", "", word)
            if word in users:  # SOMEONE MENTIONED SOMEONE
                if userData.has_key(user):  # This user is already set up
                    if userData[user]["data"].has_key(
                        word
                    ):  # This user has mentioned this person before
                        userData[user]["data"][word] += 1
                    else:  # This user never mentioned this person before
                        userData[user]["data"][word] = 1
                    # give both the target and mentioner a point
                else:  # This user was never set up
                    userData[user] = {}  # make it a dictionary!
                    userData[user]["data"] = {}
                    userData[user]["data"][word] = 1
                    userData[user]["score"] = 0
                    userData[user]["id"] = len(
                        d3data["nodes"]
                    )  # so we know how to match people during the links phase
                    d3data["nodes"].append({"name": user, "group": 1})
                if not userData.has_key(
                    word
                ):  # check if the target has not been set up
                    userData[word] = {}
                    userData[word]["data"] = {}
                    userData[word]["score"] = 0
                    userData[word]["id"] = len(d3data["nodes"])
                    d3data["nodes"].append({"name": word, "group": 1})
                userData[user]["score"] += 1
                userData[word]["score"] += 1

d3data["links"] = []
# Now connect all the pople to their stuff
for user, values in userData.iteritems():
    # give the user a 'group' based on their total score
    d3data["nodes"][values["id"]]["group"] = int(math.ceil(math.log(values["score"])))
    besties = sorted(values["data"].items(), key=operator.itemgetter(1), reverse=True)[
        0:MAX_NODES
    ]  # ONLY the top besties
    for target, score in besties:
        try:
            print(
                "Adding link from "
                + user
                + " ("
                + str(values["id"])
                + ") to "
                + target
                + " ("
                + str(userData[target]["id"])
                + ") with strength "
                + str(score)
            )
            d3data["links"].append(
                {
                    "source": values["id"],
                    "target": userData[target]["id"],
                    "value": math.ceil(math.sqrt(score)) * 2,
                }
            )
        except KeyError:
            print("! Error when trying to link " + user + " to " + target)
            continue
    if len(values["data"]) > MAX_NODES:
        print(
            "  ...ignoring "
            + str(len(values["data"]) - MAX_NODES)
            + " more connections from "
            + user
        )

d3Circle = {}
d3Circle["names"] = [""] * len(userData)
d3Circle["matrix"] = [[0] * len(userData)] * len(userData)

for user, values in userData.iteritems():
    d3Circle["names"][values["id"]] = user
    for name, score in values["data"].iteritems():
        d3Circle["matrix"][values["id"]][userData[name]["id"]] = (
            score if score > 1 else 0
        )

with open(outfile + ".tmp", "w") as tmpFile:
    tmpFile.write(json.dumps(d3data))
shutil.move(outfile + ".tmp", outfile)

with open(outCircle + ".tmp", "w") as tmpFile:
    tmpFile.write(json.dumps(d3Circle))
shutil.move(outCircle + ".tmp", outCircle)
