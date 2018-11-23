#!/usr/bin/python
import random
import inflect
import quote_puzzle
import dict_puzzle

p = inflect.engine()
primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
fuzz_amount = 3


def make_puzzle(obfuscate=True):
    answer = 0
    bonus = 0
    puzzle = random.choice(
        [
            "Prove you're not a robot: ",
            "Are you a robot?: ",
            "Anti-bot check: ",
            "Counter-cnd0rphant measures: ",
            "Cosn0k countermeasures: ",
            "Anti-tilde7hief precautions: ",
            "Pro-l0gin challenge: ",
            "Riddle me this: ",
            "Would you like to play a game? ",
            "How about this? "
        ]
    )
    puzzle += random.choice(
        [
            "What is",
            "What do you get from",
            "What do you get with",
            "What is the value of",
            "Can you answer",
            "Can you tell me",
            "Ask wiz3bot what is",
            "Does anybody know",
            "Who knows",
            "Guess what",
            "Calculate",
            "Find out"
        ]
    )
    puzzle += " "
    roll = random.randrange(0, 18)
    var1 = random.randrange(1, 10)
    var2 = random.randrange(1, 10)
    var3 = random.randrange(1, 20)
    var4 = random.randrange(1, 20)
    let1_ord = random.randrange(ord("a"), ord("z") + 1)

    if roll == 0:
        answer = var1 + var2
        puzzle += "{} {} {}".format(
            p.number_to_words(var1),
            random.choice(["and", "plus", "sum", "add"]),
            p.number_to_words(var2),
        )

    elif roll == 1:
        answer = var1 * var2
        puzzle += "{} {} {}".format(
            p.number_to_words(var1),
            random.choice(["times", "multiply", "multiplied by", "product"]),
            p.number_to_words(var2),
        )

    elif roll == 2:
        if var2 > var1:
            var1, var2 = var2, var1
        answer = var1 - var2
        puzzle += "{} {} {}".format(
            p.number_to_words(var1),
            random.choice(["minus", "subtract", "take away", "less"]),
            p.number_to_words(var2),
        )

    elif roll == 3:
        if var2 > var1:
            var1, var2 = var2, var1
        answer = var1 * 2 / var2
        puzzle += "{} {} {} (no remainder)".format(
            p.number_to_words(var1 * 2),
            random.choice(["divided by", "over"]),
            p.number_to_words(var2),
        )

    elif roll == 4:
        answer = var1 ** var2
        puzzle += "{} to the {} power".format(
            p.number_to_words(var1), p.ordinal(p.number_to_words(var2))
        )

    elif roll == 5:
        p1 = random.choice(primes)
        p2 = random.choice(primes)

        def answer(guess):
            # Check the the numbers entered are correct, regardless of order
            # or surrounding whitespace.
            attempt = sorted(word.strip() for word in guess.split(","))
            correct = sorted([str(p1), str(p2)])
            return attempt == correct

        bonus = 1
        puzzle += "{} when factored into its two primes (answer in the form of the two primes with a comma between)".format(
            p.number_to_words(p1 * p2)
        )

    elif roll == 6:
        prime = random.choice(primes)
        answer = prime % var1
        puzzle += p.number_to_words(prime) + " modulus " + p.number_to_words(var1)
    elif roll == 7:
        if let1_ord + var1 > ord("z"):
            let1_ord -= var1
        answer = chr(let1_ord + var1)
        puzzle += "letter comes {} letters after '{}'".format(
            p.number_to_words(var1), chr(let1_ord)
        )

        obfuscate = False
    elif roll == 8:
        if let1_ord - var1 < ord("a"):
            let1_ord += var1
        answer = chr(let1_ord - var1)
        puzzle += "letter comes {} letters before '{}'".format(
            p.number_to_words(var1), chr(let1_ord)
        )

        obfuscate = False
    elif roll == 9:
        answer, puzzle = quote_puzzle.get_quote()
        obfuscate = False
    elif roll == 10:
        answer = str(min(var1, var2, var3, var4))
        puzzle += "the {} of {}, {}, {}, and {}".format(
            random.choice(["smallest", "lowest"]),
            p.number_to_words(var1),
            p.number_to_words(var2),
            p.number_to_words(var3),
            p.number_to_words(var4),
        )

    elif roll == 11:
        answer = str(max(var1, var2, var3, var4))
        puzzle += "the {} of {}, {}, {}, and {}".format(
            random.choice(["biggest", "largest"]),
            p.number_to_words(var1),
            p.number_to_words(var2),
            p.number_to_words(var3),
            p.number_to_words(var4),
        )

    elif roll <= 14:  # 12-14
        answer, puzzle = dict_puzzle.get_puzzle()
        obfuscate = False
    elif roll <= 17:  # 15-17
        answer, puzzle = dict_puzzle.get_anagram()
        obfuscate = False

    # Add a question mark on the end of the question
    if puzzle[-1] != "?":
        puzzle += "?"

    if obfuscate == True:
        for _ in range(fuzz_amount):
            idx = random.randrange(len(puzzle) - 2)  # get between 0 and string length (except the ? mark)
            puzzle = "".join(
                [puzzle[0:idx], chr(random.randint(33, 126)), puzzle[idx + 1 :]]
            )
    return [puzzle, answer, bonus]
