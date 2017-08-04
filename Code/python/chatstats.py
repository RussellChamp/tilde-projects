#!/usr/bin/python
import fileinput
import json
import time
import calendar
import shutil
import re

logfile = "/home/jumblesale/Code/irc/log"
outfile = "/home/krowbar/logs/chatStats.json"
userData = {} #hash keyed by "user" that contains a start timestamp, last timestamp, last said string, chat count, letter count, and word count
                #also now happy emotes and sad emotes
rejectRegexp = "http[s]?://|[0-9]{2}[;:][0-9]{2}"
happyRegexp = ":[-]?[])}]"
sadRegexp = ":[-]?[[({]"
nameFix = {
        'archangel': 'archangelic',
        'jumblesal': 'jumblesale',
        'hardmath1': 'kc',
        'hardmath123': 'kc',
        'bendorphan': 'endorphant',
        'endorphan': 'endorphant',
        'synergian': 'synergiance'
        }

with open(logfile, "r") as log:
    lastUser = "";
    currentStreak = 1
    for line in log:
        try:
            time, user, message = line.split("\t", 3)
            time = int(time)
            if nameFix.has_key(user):
                user = nameFix[user]
            else:
                user = user.lower()
        except ValueError:
            continue #There are some bad lines in the log file that we'll ignore if we can't parse
        if user in userData:
            day = time / 86400 #seconds in a day
            if userData[user]['startTime'] == 0:
                userData[user]['startTime'] = time
            if userData[user]['lastDay'] != day:
                userData[user]['daysActive'] += 1
                userData[user]['lastDay'] = day
            if lastUser == user:
                currentStreak += 1
                if currentStreak > userData[user]['streak']:
                    userData[user]['streak'] = currentStreak
            else:
                currentStreak = 1
            if userData[user]['lastMention']:
                resTime = time - userData[user]['lastMention']
                userData[user]['responseTime'] += min(resTime, 7200) #cap the value at 2hrs, things get skewed toward the high end otherwise
                userData[user]['lastMention'] = 0

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
            userData[user]['daysActive'] = 1
            userData[user]['lastDay'] = time / 86400
            userData[user]['streak'] = 1
            userData[user]['mentions'] = 0
            userData[user]['lastMention'] = 0
            userData[user]['responseTime'] = 0
            userData[user]['botUse'] = 0
            userData[user]['happyEmotes'] = 0
            userData[user]['sadEmotes'] = 0

        lastUser = user;
        if message.rstrip() and message[0] == '!':
            userData[user]['botUse'] += 1
        if not re.search(rejectRegexp, message):
            if re.search(happyRegexp, message):
                userData[user]['happyEmotes'] += 1
            if re.search(sadRegexp, message):
                userData[user]['sadEmotes'] += 1

        try:
            if message.rstrip() and message.split()[0][-1] == ':': #last character of first word
                name = message.split()[0][0:-1]
                if user != name and userData.has_key(name):
                    userData[name]['mentions'] += 1
                    if not userData[name]['lastMention']:
                        userData[name]['lastMention'] = time
        except IndexError:
            print '##' + message + '##'
            continue


with open(outfile + ".tmp", "w") as tmpFile:
    tmpFile.write(json.dumps(userData))
shutil.move(outfile + ".tmp", outfile)
