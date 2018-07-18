#!/usr/bin/python
import random
import inflect

p = inflect.engine()
dictionary = "/usr/share/dict/american-english-small"
BAD_WORDS_FILE = "badwords.txt"

def get_wordlist():
    # I feel weird calling this "get_wordlist" when it's a generator without calling out that I do in fact realise it's weird - ~deltawitch
    with open(BAD_WORDS_FILE, "r") as fp:
        bad_words = set(fp)

    for word in open(dictionary).readlines():
        if "'" not in word and word not in bad_words:
            yield word.rstrip()

def get_puzzle():
    dict_words = list(get_wordlist())
    words = random.sample(dict_words, 3)
    key = random.randrange(0,3) #get values 1-3
    puzzle = "When alphebetized, what is the " + p.ordinal(p.number_to_words(key+1)) + " in " + ", ".join(words)
    words.sort()
    answer = words[key]
    return [answer, puzzle]

def get_anagram(maxlen = 6):
    dict_words = [word for word in get_wordlist() if len(word) > 2 and len(word) <= maxlen+1]
    word = random.choice(dict_words)
    while True:
        anagram = ''.join(random.sample(word, len(word)))
        if anagram != word:
            break
    puzzle = "Unscramble the following word: '" + anagram + "'"

    # Anagrams can have multiple answers, so we provide a check function that accepts all possibilities
    def answer_checker(guess):
        # Check for exact match
        if guess == word:
            return True
        # Bail out early if they didn't even use all the same letters
        if sorted(guess) != sorted(word):
            return False
        # Ok, gotta actually check if it's a word now
        return any(guess == item for item in get_wordlist())
    return [answer_checker, puzzle]
