#!/usr/bin/python
import fileinput
import json
import time
import calendar
import shutil

logfile = "/home/archangelic/irc/log"
# logfile = "/home/jumblesale/Code/irc/log"
outfile = "/home/krowbar/logs/chatStack.json"
chatData = {
    "hours": [],
    "regions": {},
}  # hash keyed by "region" and then hour that counts chat instances
# we only care about recent chats, let's say for the past couple weeks
oneHour = 60 * 60
oneWeek = 7 * 24 * 60 * 60
timeNow = calendar.timegm(time.gmtime())
timeCutoff = calendar.timegm(time.gmtime()) - (2 * oneWeek)

# this will eventually represent each region users are from
def getAllRegions():
    return ["unknown"]


# this will provide a way to look up what region a user is from
def getRegion(user):
    return "unknown"


# populate the hours array with time 1 hour away from each other
startTime = timeCutoff
while startTime < timeNow:
    chatData["hours"].append(startTime)
    startTime += oneHour

# populate the regions array with blank data for each region
for region in getAllRegions():
    chatData["regions"][region] = {
        "name": region,
        "values": [0] * len(chatData["hours"]),
    }

with open(logfile, "r") as log:
    hourIdx = (
        0
    )  # starting with the oldest time slot, we will count instances of user chatting
    for line in log:
        try:
            time, user, message = line.split("\t", 3)
            time = int(time)
        except ValueError:
            continue  # There are some bad lines in the log file that we'll ignore if we can't parse
        if time > timeCutoff:
            region = getRegion(user)
            while (
                time > chatData["hours"][hourIdx] + oneHour
            ):  # we are past the current hour idx, move ahead until we find the right idx
                hourIdx += 1
                if hourIdx >= len(chatData["hours"]):
                    break
                    # uh oh! somehow we are parsing a line from the future! we're in pretty bad shape!
            # hourIdx should now be a good value
            chatData["regions"][region]["values"][
                hourIdx
            ] += 1  # increment the user region's count for the current hour

with open(outfile + ".tmp", "w") as tmpFile:
    tmpFile.write(json.dumps(chatData))
shutil.move(outfile + ".tmp", outfile)
