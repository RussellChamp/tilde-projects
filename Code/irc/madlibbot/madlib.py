#!/usr/bin/python

import collections
import glob
import inflect
import random
import re

p = inflect.engine()
file_pattern = "/home/*/madlibs/*.madlib"
file_regex = re.compile(r"^/home/(.*?)/.*/([^/]*)\.madlib$")
word_regex = re.compile(r"{{(.*?)(#.*?)?(\|.*)?}}")
word_replace_regex = re.compile(r"^(.*)#(\d*)$")

# Take a file path and return a tuple with the title and original path
def munge_story(file_name):
    match = re.match(file_regex, file_name)
    count = count_words_file(file_name)
    return (
        "'" + match.group(2).replace("_", " ") + "' by ~" + match.group(1),
        match.group(0),
        count,
    )


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
    # words that have a '#' part and match should only be counted once
    count = 0
    repeats = []
    for match in re.finditer(word_regex, story):
        if match.group(2) is None:  # the '#' part
            count += 1
        elif match.group(1) + match.group(2) not in repeats:
            count += 1
            repeats.append(match.group(1) + match.group(2))
    return count


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


# Using a query phrase, replace a word and return the entire story body
def replace_word(story, query, word):
    rquery = word_regex.search(query)
    # '{{foo#bar|baz|bang}}' => ('foo', '#bar', '|baz|bang')
    pipes = [
        p.lower()
        for p in (rquery.group(3) if rquery.group(3) is not None else "")
        .strip("|")
        .split("|")
    ]
    munged_word = process_pipes(word, pipes)
    story = story.replace(query, munged_word, 1)

    if rquery.group(2) is not None:  # if there is a '#' part we replace all instances
        print("Looking for {{" + rquery.group(1) + rquery.group(2) + ".*?}}")
        others = re.findall(r"{{" + rquery.group(1) + rquery.group(2) + ".*?}}", story)
        if len(others) > 0:
            story = replace_word(
                story, others[0], word
            )  # iteratively replace the next instance

    return story


# Modify user input based on certain modifying pipes
def process_pipes(word, pipes):
    for pipe in pipes:
        try:
            word = {
                "upper": lambda word: word.upper(),
                "lower": lambda word: word.lower(),
                "title": lambda word: word.title(),
                "numeric": lambda word: p.number_to_words(word),
                "ordinal": lambda word: p.ordinal(word),
                collections.defaultdict: lambda word: word,
            }[pipe](word)
        except Exception:
            pass  # just keep going if an error occurs processing a pipe
    return word


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
            yield " ".join(words)
            words = []
            words_length = 0
            word = word[splitsize:]
        if words_length + len(word) + 1 > max_size:
            yield " ".join(words)
            words = []
            words_length = 0
        words.append(word)
        words_length += len(word) + 1  # For the space
    yield " ".join(words)  # For any words left over


# Open a story file and ask for the parts
def make_story(storyFile):
    with open(storyFile, "r") as storyFile:
        story = storyFile.read()
        match = word_regex.search(story)
        while match is not None:
            word = raw_input("Give me {}: ".format(match.group(1)))
            print("Replacing '{}' with '{}'".format(match.group(0), word))
            print(story)
            story = re.sub(match.group(0), word, story, 1)
            match = word_regex.search(story)
        print(story)


def start():
    stories = find_stories(20, True)
    if len(stories) == 0:
        print("Sorry, no stories found. :/")
        return

    input = -1
    while input < 0 or input >= len(stories):
        for idx, story in enumerate(stories):
            print("[{}] {}".format(idx, story[0]))
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
