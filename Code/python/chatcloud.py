#!/usr/bin/python
import fileinput
import json
import time
import calendar
import re
import shutil

logfile = "/home/jumblesale/Code/irc/log"
outfile = "/home/krowbar/logs/chatcloud.json"
bannedWordsFile = "/home/krowbar/Code/python/bannedWords"
wordData = {} # keyed by "word" that contains a count
#we only care about recent chats, let's say for the past two weeks
timeCutoff = calendar.timegm(time.gmtime()) - (2 * 7 * 24 * 60 * 60)
minOccurance = 10
bannedWords = open(bannedWordsFile).read().splitlines()

with open(logfile, "r") as log:
    for line in log:
        try:
            time, user, message = line.split("\t", 3)
            time = int(time)
        except ValueError:
            continue #There are some bad lines in the log file that we'll ignore if we can't parse
        if time > timeCutoff:
            for word in re.sub('[\'\";:,.?!*&^\-()\[\]]', '', message).lower().split():
                if word in bannedWords:
                    continue
                #if the word already exists in the list
                if word in wordData:
                    wordData[word] += 1
                else: #if they are new
                    wordData[word] = 1
                    #print "Added word: " + word
wordData = {i:wordData[i] for i in wordData if wordData[i] >= minOccurance }
with open(outfile + ".tmp", "w") as tmpFile:
    tmpFile.write(json.dumps(wordData))
shutil.move(outfile + ".tmp", outfile)
