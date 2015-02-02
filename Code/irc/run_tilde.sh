#!/bin/bash

nohup ./tildebot.py -s 127.0.0.1 -n tildebot -c \#tildetown >> tildelog 2>> tildelog &
#nohup ./tildebot.py -s 127.0.0.1 -n tildebot -c \#bot_test >> tildelog 2>> tildelog &
