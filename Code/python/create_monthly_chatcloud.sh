#!/bin/bash
START=$((`date +%s` - 2678400))
END=`date +%s`
MONTH=`date -d yesterday +_%Y_%m`
DATE=`date -d yesterday +%b\ %Y`
OUT=/home/krowbar/logs/chatcloud${MONTH}.json
DIR=/home/krowbar/public_html/data
PAGE=/home/krowbar/public_html/chatcloud/index.html
LINE=16

/usr/bin/python /home/krowbar/Code/python/chatcloud2.py -timeend $END -timestart $START -outfile $OUT
ln -s $OUT $DIR

sed "${LINE}i  <option value=\"${MONTH}\">${DATE}</option>" < $PAGE > $PAGE.tmp
mv $PAGE.tmp $PAGE
