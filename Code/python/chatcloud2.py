#!/usr/bin/python
import fileinput
import json
import time
import calendar
import re
import shutil
import argparse
import logging, sys

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

parser = argparse.ArgumentParser(
    description="Generate word cloud data based off of irc chat logs"
)
parser.add_argument(
    "-logfile", help="irc log file to read from", default="/home/archangelic/irc/log"
)
parser.add_argument("-outfile", help="output file to write to", default="")

parser.add_argument(
    "-timeend",
    type=int,
    help="end time of the word cloud (in epoch time)",
    default=calendar.timegm(time.gmtime()),
)
parser.add_argument(
    "-timestart",
    type=int,
    help="start time of the word cloud (in epoch time)",
    default=-1,
)

parser.add_argument(
    "-bannedUsersFile",
    help="file containing list of banned users",
    default="/home/krowbar/Code/python/bannedUsers",
)
parser.add_argument(
    "-bannedWordsFile",
    help="file containing list of banned words",
    default="/home/krowbar/Code/python/bannedWords",
)

parser.add_argument(
    "-minLength",
    type=int,
    help="minimum size of words to include in the cloud",
    default=3,
)
parser.add_argument(
    "-minOccurrence",
    type=int,
    help="the minimum occurence of a word to include it in the cloud",
    default=3,
)

args = parser.parse_args()

wordData = {}  # keyed by "word" that contains a count
# we only care about recent chats, let's say for the past sixteen hours

args.timestart = (
    args.timestart if args.timestart != -1 else args.timeend - (16 * 60 * 60)
)
# timeCutoff = calendar.timegm(time.strptime("1 Oct 16", "%d %b %y"))
logging.info(
    "Generating word cloud based off words from "
    + str(args.timestart)
    + " to "
    + str(args.timeend)
)

bannedWords = open(args.bannedWordsFile).read().splitlines()
bannedUsers = open(args.bannedUsersFile).read().splitlines()

with open(args.logfile, "r") as log:
    for line in log:
        try:
            time, user, message = line.split("\t", 3)
            time = int(time)
        except ValueError:
            continue  # There are some bad lines in the log file that we'll ignore if we can't parse
        if user in bannedUsers:
            continue  # We don't care what they say
        if time >= args.timestart and time <= args.timeend:
            # print "Processing line from " + user + " at " + str(time)
            for word in (
                re.sub("['\"\`\/\\;:,.?!*&^\-()<>\{\}|_\[\]0-9]", " ", message)
                .lower()
                .split()
            ):
                # changing symbols into spaces instead of stripping them avoids compounded words
                if len(word) < args.minLength or word in bannedWords:
                    # print "Rejecting " + word
                    continue
                # if the word already exists in the list
                if word in wordData:
                    wordData[word] += 1
                else:  # if they are new
                    wordData[word] = 1
                    # print "Added word: " + word
wordData = {i: wordData[i] for i in wordData if wordData[i] >= args.minOccurrence}
if len(wordData) == 0:
    wordData = {"NOTHING": 1, "INTERESTING": 1, "TODAY": 1}
if args.outfile == "":
    print(json.dumps(wordData))
else:
    with open(args.outfile + ".tmp", "w") as tmpFile:
        tmpFile.write(json.dumps(wordData))
    shutil.move(args.outfile + ".tmp", args.outfile)
