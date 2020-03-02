#!/usr/bin/python3
import fileinput
import json
import time
import calendar
import re
import shutil
import argparse
import logging, sys
import math
import os

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

parser = argparse.ArgumentParser(
    description="Generate word list data based off of aggregate irc chat logs"
)

parser.add_argument(
    "-outfile",
    help="output file to write to",
    default="/home/krowbar/logs/chatcloud_aggregate.json"
)

parser.add_argument(
    "-logpath",
    type=str,
    help="where the log files are kept",
    default="/home/krowbar/logs",
)
parser.add_argument
args = parser.parse_args()

chatData = {
    "columns": [ "__TIMESTAMP__" ],
    "data": []
}

logging.info(
    "Generating word graph based off words from " + args.logpath
)

logs = sorted([f for f in os.listdir(args.logpath) if re.match(r'chatcloud_[0-9]{4}_[0-9]{2}.json', f)])
for log in logs:
    date = re.findall("[0-9]{4}_[0-9]{2}", log)[0]
    year = re.findall("[0-9]{4}", date)[0]
    if year < '2019':
        continue
    print("Processing: {}...".format(log), end='')

    logData = [ date ]
    with open(os.path.join(args.logpath, log), "r") as logfile:
        j = json.load(logfile);
        for col in chatData['columns']:
            if col in j.keys():
                logData.append(j[col])
            elif col is not "__TIMESTAMP__":
                logData.append(0)

        for key in j.keys():
            if key in chatData['columns']:
                continue
            else:
                chatData['columns'].append(key)
                for d in chatData['data']:
                    d.append(0)
                # append a 0 in each other chatData.data rows
                logData.append(j[key])

        chatData['data'].append(logData);
        print(" Columns: {}, Records: {}".format(len(chatData['columns']), len(logData)))

with open(args.outfile + ".tmp", "w") as tmpFile:
    tmpFile.write(json.dumps(chatData))
    # shutil.move(args.outfile + ".tmp", args.outfile)
    print("Dumped {} records to {}".format(len(chatData['columns']), args.outfile))
