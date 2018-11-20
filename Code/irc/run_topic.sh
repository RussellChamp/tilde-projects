#!/bin/bash
if [[ ! `pidof -sx topicbot.py` ]]; then
  nohup ./topicbot.py -s 127.0.0.1:6667 -n topicbot -c \#tildetown \#bots >> topiclog 2>> topiclog &
fi
#nohup ./topicbot.py -s 127.0.0.1:6667 -n topicbot -c \#bot_test \#bots >> topiclog 2>> topiclog &
#./topic_bot.py -s 127.0.0.1 -n topic_bot -c \#bot_test
