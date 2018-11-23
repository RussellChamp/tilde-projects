#!/bin/bash

if [[ ! `pidof -sx madlibbot.py` ]]; then
  nohup ./madlibbot/madlibbot.py -s 127.0.0.1:6667 -n madlibbot -c \#bots \#madlibs >> madliblog 2>> madliblog &
  echo "Starting madlibbot"
else
  echo "madlibbot has already been started"
fi
