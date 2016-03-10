#!/bin/bash

if [[ ! `pidof -sx banterbot.py` ]]; then
  nohup ./banterbot.py -s 127.0.0.1 -n banterbot -c \#tildetown >> banterlog 2>> banterlog &
  echo "Starting banterbot"
#nohup ./banterbot.py -s 127.0.0.1 -n banterbot -c \#bot_test >> banterlog 2>> banterlog &
else
  echo "Banterbot has already been started"
fi
