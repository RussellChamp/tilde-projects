#!/bin/bash
if [[ ! `pidof -sx tildebot.py` ]]; then
  echo "Starting tildebot"
  nohup ./tildebot.py -s 127.0.0.1:6667 -n tildebot -c \#tildetown \#bots >> tildelog 2>> tildelog &
  #nohup ./tildebot.py -s 127.0.0.1:6667 -n tildebot -c \#bots >> tildelog 2>> tildelog &
else
  echo "Tildebot has already been started"
fi
