file=$1
cowtype=`/usr/games/cowsay -l | tail -n +2 | tr ' ' '\n' | sort -R | head -1` 
beats=`echo "x = (\`date +%s\` + 3600) % 86400; scale=3; x / 86.4" | bc`

echo '3 1' > $file
/usr/games/cowsay -W 24 -f $cowtype The time is @$beats >> $file
