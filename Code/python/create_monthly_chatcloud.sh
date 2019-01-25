#!/bin/bash
START=$((`date +%s` - 2678400)) # 31 days
END=`date +%s`
MONTH=`date -d yesterday +_%Y_%m`
DATE=`date -d yesterday +%b\ %Y`
OUT=/home/krowbar/logs/chatcloud${MONTH}.json
DIR=/home/krowbar/public_html/data
PAGE=/home/krowbar/public_html/chatcloud/index.html
LINE=16 # This is the magic line number where we want to insert the new option in the dropdown

/usr/bin/python /home/krowbar/Code/python/chatcloud2.py -timeend $END -timestart $START -outfile $OUT -timestamp "month"
if [ ! -e ${DIR}/chatcloud${MONTH}.json ]
then
  ln -s $OUT $DIR
  echo Creating link to $OUT in $DIR
else
  echo Skipping linking... already exists in $DIR
fi

sed "${LINE}i  <option value=\"${MONTH}\">${DATE}</option>" < $PAGE > $PAGE.tmp
echo Added option for ${DATE} in $PAGE

mv $PAGE.tmp $PAGE
