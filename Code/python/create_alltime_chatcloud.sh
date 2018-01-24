#!/bin/bash
START=0
END=`date +%s`
OUT=/home/krowbar/logs/chatcloud_all_time.json
DIR=/home/krowbar/public_html/data

/usr/bin/python /home/krowbar/Code/python/chatcloud2.py -timeend $END -timestart $START -outfile $OUT
