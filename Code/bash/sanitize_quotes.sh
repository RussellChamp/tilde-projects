#!/bin/bash

quotesFile="/home/karlen/irc/quotes.txt"
outFile="/home/krowbar/scratch/quotes.txt"

cat $quotesFile | grep -v '^[-/]' > $outFile
