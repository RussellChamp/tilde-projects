#!/usr/bin/python3

# Import some necessary libraries.
import random
import re
import inflect
import util.puzzle

p = inflect.engine()
challenges = {}
SCORE_FILE = "/home/krowbar/Code/irc/data/tildescores.txt"
JACKPOT_FILE = "/home/krowbar/Code/irc/data/tildejackpot.txt"
JACKPOT_MIN = 3
DEBUG = False
GOOD_CHAN = "#bots" # The name of the "good" channel that the bot is allowed to run in

def too_recent(time1, time2):
    return int(float(time1)) - int(float(time2)) < 60 * 60


def get_positive():
    return random.choice(
        [
            "Yes",
            "Yep",
            "Yeppers",
            "Correct",
            "You got it",
            "Yeah",
            "Right on",
            "Uh-huh",
            "Positive",
            "Totally right",
            "Close enough",
            "That's it",
            "Winner, winner",
            "Bingo",
            "Affirmative",
        ]
    )


def get_negative():
    return random.choice(
        [
            "No",
            "Nope",
            "Sorry",
            "Wrong",
            "Nuh-uh",
            "Negatory",
            "Incorrect",
            "Not today",
            "Try again",
            "Maybe later",
            "Maybe next time",
            "Probably not",
            "Answer hazy",
            "Not quite",
            "Not even close",
            "Not for you",
            "I think not",
            "Wait... uh maybe?",
            "It could have been",
            "It should have been",
            "Whoops",
            "SegFault: Insufficient Tildes",
            "Wait, what did you guess?"
        ]
    )


def get_superlative(score):
    if score > 4:
        return random.choice(
            [
                "super cool",
                "totally rad",
                "extraordinary",
                "dynomite",
                "#topdrawer",
                "a #TopLad",
                "the cat's meow",
                "a tilde town hero",
                "my favorite person",
                "incredibly lucky",
                "unbelievable",
                "a tilde town hunk",
                "could bring all the boys to the yard",
                "worth twice their weight in gold",
                "the hero we need",
                "no ordinary townie",
                "the bot whisperer",
                "probably predicting rng",
            ]
        )
    elif score > 2:
        return random.choice(
            [
                "really cool",
                "pretty neat",
                "rather nice",
                "a dynamic doggo",
                "radical",
                "intense",
                "pretty lucky",
                #"knows the territory",
                #"has what it takes",
                #"has mad skillz",
                "going the distance",
                "a hard worker",
                "my sunshine",
                "ready to rumble",
                "better than sliced bread",
                "main protagonist material",
                "right as rain",
                "a puzzle prophet",
                "a counter-captcha expert",
            ]
        )
    else:
        return random.choice(
            [
                "cool",
                "nice",
                "acceptible",
                "good enough",
                "a promising pupper",
                "better than a horse",
                "swell",
                "a little lucky",
                "just credible",
                "my friend",
                "probably not a robot",
                "valuable to the team",
                "now trending",
                "on your way up",
                "credit to team",
                "a net positive",
                "groovy",
                "competent",
                "not wrong",
                "on the right track",
            ]
        )


def get_bad_thing():
    return random.choice(
        [
            "is a meanie",
            "mugs me right off",
            "miffed me off",
            "is worse than a horse",
            "smells like a ghost",
            "probably didn't bathe today",
            "probably shakes babies",
            "didn't guess hard enough",
            "isn't lucky",
            "smells of elderberries",
            "should reconsider their life choices",
            "did't believe in the heart of the tilde",
            "came to the wrong side of town",
            "should have stopped while they were ahead",
            "requires annotations from an authoratative source",
            "could have been a contender",
            "spreads vicious rumors",
            "drank my milkshake",
            "is probably cheating",
            "is trying too hard",
            "didn't really try",
            "should try harder",
            "caught me in a bad mood",
            "should have gone with their first choice",
            "did not receive IFR clearance from tower",
            "was tardy for class",
            "is on double secret probation",
            "forgot their keys",
            "forgot to bribe me",
            "forgot to close the door",
            "waited too long",
            "doesn't call me on my cellphone",
            "isn't wearing a seatbelt",
            "didn't courtesy flush",
            "asked a bot for answers",
            "was right but I didn't feel like it",
            "is right on opposite day",
            "actually answered the last question",
            "has their pants on backwards",
            "forgot their own name",
            "got me really confused"
        ]
    )


def get_prize(user, isHuman, bonus=0):
    prizes = [1] * 8 + [2] * 4 + [3] * 2 + [5] * isHuman  # no 5pt prize for non-humans
    prize = random.choice(prizes) + bonus
    if (
        random.randint(1, 10) > 6 - 4 * isHuman
    ):  # 80% of the time it's a normal prize (40% for not humans)
        return [
            prize,
            "{}: {}! You are {} and get {} tildes!".format(
                user,
                (get_positive() if isHuman else get_negative()),
                get_superlative(prize),
                p.number_to_words(prize),
            ),
        ]
    else:  # 20% of the time its a jackpot situation
        with open(JACKPOT_FILE, "r+") as jackpotfile:
            jackpot = int(jackpotfile.readline().strip("\n"))
            jackpotfile.seek(0)
            jackpotfile.truncate()
            if (
                random.randint(1, 10) > 1 or not isHuman
            ):  # 90% of the time it's a non-prize. non-humans never win jackpot
                new_jackpot = jackpot + max(1, prize)
                jackpotfile.write(
                    str(new_jackpot)
                )  # increase the jackpot by the prize size
                return [
                    0,
                    "{} {} and gets no tildes! (Jackpot is now {} tildes)".format(
                        user, get_bad_thing(), new_jackpot
                    ),
                ]
            else:  # hit jackpot!
                jackpotfile.write(str(JACKPOT_MIN))
                return [
                    jackpot,
                    "{} hit the jackpot and won **{}** tildes!".format(
                        user, p.number_to_words(jackpot)
                    ),
                ]


def show_jackpot():
    with open(JACKPOT_FILE, "r") as jackpotfile:
        jackpot = int(jackpotfile.readline().strip("\n"))
        return "The jackpot is currently {} tildes!".format(p.number_to_words(jackpot))


def give_tilde(user, time, human, bonus=0):
    found = False
    with open(SCORE_FILE, "r+") as scorefile:
        scores = scorefile.readlines()
        scorefile.seek(0)
        scorefile.truncate()
        message = ""
        for score in scores:
            name, score_on_file, timestamp = score.strip("\n").split("&^%")
            if name == user:
                found = True
                if too_recent(time, timestamp) and not DEBUG:
                    message = "{} asked for a tilde too recently and {}. Try again later.".format(user, get_bad_thing())
                else:
                    prizevalue, prizetext = get_prize(user, human, bonus)
                    score = "{}&^%{}&^%{}\n".format(
                        user, str(int(score_on_file) + prizevalue), time
                    )
                    message = prizetext
            scorefile.write(score)
        if not found:
            prizevalue, prizetext = get_prize(user, True, bonus)
            scorefile.write("{}&^%{}&^%{}\n".format(user, str(prizevalue + 1), time))
            message = "Welcome to the tilde game, {}! Here's {} free tildes to start you off.".format(user, p.number_to_words(prizevalue + 1))

        return message


def show_tildescore(user):
    with open(SCORE_FILE, "r") as scorefile:
        for _idx, score in enumerate(scorefile):
            record = score.strip("\n").split("&^%")
            if record[0] == user:
                return "{} has {} tildes!".format(user, p.number_to_words(record[1]))
        # person has not played yet
        return "{} has no tildes yet!".format(user)


def challenge(channel, user, time):
    global challenges
    challenge = util.puzzle.make_puzzle()
    challenges[user] = challenge[1:]
    return "{}: {}".format(user, challenge[0])

def valid_answer(answer, guess):
    guess = guess.lower();
    if callable(answer):
        return answer(guess)
    else:
        # convert the guess and answer to just alphanumeric values. some
        # "answers" acidentally have punctuation or other things in them
        guess = re.sub(r'\W+', '', guess)
        answer = re.sub(r'\w+', '', str(answer).lower())
        return (msg == answer or msg == p.number_to_words(answer))

def challenge_response(user, time, msg):
    global challenges
    # print(msg)
    response = ""
    if user in challenges:
        answer, bonus = challenges[user]
        if valid_answer(answer, msg):
            response = give_tilde(user, time, True, bonus)
        else:
            response = give_tilde(user, time, False, 0)
        del challenges[user]
        # delete the user from challenges either way
    return response
