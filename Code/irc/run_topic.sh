#!/bin/bash

nohup ./topicbot.py -s 127.0.0.1 -n topicbot -c \#tildetown >> log 2>> log &
#nohup ./topicbot.py -s 127.0.0.1 -n topicbot -c \#bot_test >> log 2>> log &
#./topic_bot.py -s 127.0.0.1 -n topic_bot -c \#bot_test
