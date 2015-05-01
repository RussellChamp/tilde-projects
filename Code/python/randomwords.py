#!/usr/bin/python
import fileinput
import random
import sys
import argparse

parser = argparse.ArgumentParser(description='Print some random dictionary words.')
parser.add_argument('-d', dest='dictionary', metavar='DICT',
        help='supply a dictionary', default='/usr/share/dict/american-english-large')
parser.add_argument('-c', dest='count', type=int,
        help='specify how many words you want per line', default=10)
parser.add_argument('-l', dest='lines', type=int,
        help='specify how many lines of random words you want', default=1)
parser.add_argument('--no-appos', action='store_true',
        help='remove words with appostrophes')
parser.add_argument('--no-proper', action='store_true',
        help='remove words that start with a capital letter')

args = parser.parse_args()
#print args

with open(args.dictionary, "r") as wordsfile:
    words = wordsfile.readlines()
    if(args.no_appos):
        words[:] = [word for word in words if word.find('\'') == -1]
    if(args.no_proper):
        words[:] = [word for word in words if not word[0].isupper()]
    for _ in range(0, args.lines):
        print ' '.join([w.strip("\n") for w in  random.sample(words, args.count)])
