#!/usr/bin/python
import fileinput
import json
import time
import calendar
import shutil

logfile = "/home/jumblesale/Code/irc/log"
outfile = "/home/krowbar/logs/chatStats.json"
userData = {} #hash keyed by "user" that contains a start timestamp, last timestamp, last said string, chat count, letter count, and word count

with open(logfile, "r") as log:
    for line in log:
        try:
            time, user, message = line.split("\t", 3)
            time = int(time)
        except ValueError:
            continue #There are some bad lines in the log file that we'll ignore if we can't parse
        if user in userData:
            if userData[user]['startTime'] == 0:
                userData[user]['startTime'] = time
            userData[user]['endTime'] = time
            #userData[user]['lastSaid'] = message
            userData[user]['lineCount'] += 1
            userData[user]['wordCount'] += len(message.split())
            userData[user]['charCount'] += len(message)
        else: #if they are new
            userData[user] = {}
            userData[user]['startTime'] = time
            userData[user]['endTime'] = time
            #userData[user]['lastSaid'] = message
            userData[user]['lineCount'] = 1
            userData[user]['wordCount'] = len(message.split())
            userData[user]['charCount'] = len(message)


with open(outfile + ".tmp", "w") as tmpFile:
    tmpFile.write(json.dumps(userData))
shutil.move(outfile + ".tmp", outfile)
