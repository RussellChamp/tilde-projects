#!/bin/bash

if [[ ! `pidof -sx banterbot.py` ]]; then
  #nohup ./banterbot.py -s 127.0.0.1:6667 -n banterbot -c \#tildetown \#bots >> banterlog 2>> banterlog &
  echo "Starting banterbot"
  nohup ./banterbot.py -s 127.0.0.1:6667 -n banterbot -c \#tildetown \#bots >> banterlog 2>> banterlog &
else
  echo "Banterbot has already been started"
fi
