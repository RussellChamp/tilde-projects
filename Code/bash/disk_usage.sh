#!/bin/bash

file=/home/krowbar/logs/du_log.json
date=`date +%s`
du_threshold=200

#prepare log file
if [ -a "$file" ]
then
  echo "Appending to existing log file: $file"
  head -n -1 $file > ${file}.swp #remove trailing "]" from last line
  mv ${file}.swp ${file}
  echo "  ," >> $file
else
  echo "Creating new log file: $file"
  touch $file
  echo "[" >> $file
fi

#set up new object
echo "  {" >> $file
echo "    \"date\": $date," >> $file
echo "    \"data\": [" >> $file

add_comma=false
for user_dir in /home/*
do

  user="~${user_dir#/home/}"
  disk_usage=`du -s $user_dir 2> /dev/null | cut -f 1`
  file_count=`find $user_dir -type f 2> /dev/null | wc -l`

  if [ "$disk_usage" -gt "$du_threshold" ]
  then

    if ${add_comma}
    then
      echo "," >> $file
    else
      add_comma=true
    fi
    echo -n "      { \"user\": \"${user}\", \"du\": ${disk_usage}, \"files\": ${file_count} }" >> $file
  fi
done

echo -e "\n    ]" >> $file #close new object data
echo "  }" >> $file #close new object
echo "]" >> $file #close json array
