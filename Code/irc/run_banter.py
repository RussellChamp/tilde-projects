#!/bin/bash

nohup ./banterbot.py -s 127.0.0.1 -n banterbot -c \#tildetown >> banterlog 2>> banterlog &
#nohup ./banterbot.py -s 127.0.0.1 -n banterbot -c \#bot_test >> banterlog 2>> banterlog &
#./topic_bot.py -s 127.0.0.1 -n topic_bot -c \#bot_test
