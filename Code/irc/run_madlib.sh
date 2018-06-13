#!/bin/bash

if [[ ! `pidof -sx madlibbot.py` ]]; then
  nohup ./madlibbot/madlibbot.py -s 127.0.0.1 -n madlibbot -c \#madlibs >> madliblog 2>> madliblog &
  echo "Starting madlibbot"
else
  echo "madlibbot has already been started"
fi
