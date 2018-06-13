#!/usr/bin/python

import glob
import random
import re

file_pattern = "/home/*/madlibs/*.madlib"
file_regex = re.compile(r'^/home/(.*?)/.*/([^/]*)\.madlib$')
word_regex = re.compile(r'{{(.*?)}}')

# Take a file path and return a tuple with the title and original path
def munge_story(file_name):
    match = re.match(file_regex, file_name)
    count = count_words_file(file_name)
    return ("'" + match.group(2).replace('_', ' ') + "' by ~" + match.group(1), match.group(0), count)

# Retrive a list of all madlib story files
def find_stories(limit=999, shuffle=False):
    files = glob.glob(file_pattern)
    if shuffle == True:
        files = random.sample(files, max(1, min(limit, len(files))))
    else:
        files = files[:limit]
    return map(munge_story, files)

# Count the number of replacable words in the story
def count_words(story):
    return len(word_regex.findall(story))

# Count the number of replacable words in the story when given a file path
def count_words_file(storyPath):
    with open(storyPath, "r") as storyFile:
        story = storyFile.read()
        return count_words(story)

# Get the next replaceable word in the story. Includes full token and just the word
# If you specify rand as True, it will get a random word instead of the next one
def find_next_word(story, rand=False):
    matches = list(word_regex.finditer(story))
    if len(matches) == 0:
        return None
    match = matches[0]
    if rand is True:
        match = random.choice(matches)

    return (match.group(0), match.group(1))

# Replace a word and return the entire story body
def replace_word(story, query, word):
    return story.replace(query, word, 1)
    #return re.sub(query, word, story, 1)

# A helper function that will split the story up into chat-printable lengths
def yield_lines(line, max_size):
    words = []
    words_length = 0
    # Add words to the words line untill we run out of space
    for word in line.split():
        # If the next word itself is longer thatn max_size, we'll have to chop it up
        while len(word) > max_size:
            splitsize = max_size - words_length - 1
            words.append(word[:splitsize] + "-")
            yield ' '.join(words)
            words = []
            words_length = 0
            word = word[splitsize:]
        if words_length + len(word) + 1 > max_size:
            yield ' '.join(words)
            words = []
            words_length = 0
        words.append(word)
        words_length += len(word) + 1 # For the space
    yield ' '.join(words) # For any words left over

# Open a story file and ask for the parts
def make_story(storyFile):
    with open(storyFile, "r") as storyFile:
        story = storyFile.read()
        match = word_regex.search(story)
        while match is not None:
            word = raw_input('Give me {}: '.format(match.group(1)))
            print "Replacing '{}' with '{}'".format(match.group(0), word)
            print story
            story = re.sub(match.group(0), word, story, 1)
            match = word_regex.search(story)
        print story

def start():
    stories = find_stories(20, True)
    if len(stories) == 0:
        print "Sorry, no stories found. :/"
        return

    input = -1
    while input < 0 or input >= len(stories):
        for idx, story in enumerate(stories):
            print "[{}] {}".format(idx, story[0])
        input = raw_input("Which story would you like?: ")
        try:
            # Try to convert the string input into a number
            input = int(input)
        except:
            # If they put something stupid in, treat it as a -1 and ask for
            # input again
            input = -1
    # Call make_story with the file path of the selected story
    make_story(stories[input][1])

if __name__ == "__main__":
    start()
