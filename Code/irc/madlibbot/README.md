# MadLibs
Madlibs is a game where a player is asked for many different words that are
then inserted into an existing story template. Using different words results
in very different stories!

The Madlib library contains several functions that assist in reading a .madlib
files, querying a user for input, and constructing a resulting story.

## MadLibBot
Madlibbot is an IRC bot that utilizes the madlibs library to play MadLibs in
an IRC channel.

## Usage
The madlibbot resides in the "#madlibs" channel on the tilde.town server.
Saying "madlibbot: startgame" will start a new game of madlibs
When asked for a word, reply with "madlibbot: WORD". This is so multiple
players may banter in a channel without accidentally answering the bot.
Use the command "madlibbot: !quit" to end a game prematurely.

## Format
If you would like to make your own stories discoverable by madlibbot, create a
directory named "madlibs" in your home directory (eg "/home/krowbar/madlibs").
Inside, add story templates that have the extension ".madlib" (eg
"My_Good_Story.madlib"). Underscores will be changed to spaces when displayed
in IRC.
MadLib files are plain text and use double mustaches to denote words that will
be filled in by a user. An example is below:

* Short_Story.madlib
> This is a {{an adjective}} story.

When this story is run, the bot will ask users the following:
> madlibbot: Give me an adjective:

and continue asking for word replacement until it runs out of words to replace.

# Future Plans
* Allow users to specify the full path to a madlib file.
  * Make sure you filter only "\*.madlib" files so you don't accidentally grant elevated read permissions!
* Allow story writers the ability to specify that a single answer should be used multiple times in a story
  * Maybe specified like {{#a noun#}} or {{#a noun#4}}
* Create word-munging options that can be specified for a word to modify given user input
  * Capital - convert "foo" to "Foo"
  * AllCaps - convert "bar" to "BAR"
  * Numeric - convert "3" to "three"
  * Ordinal - convert "3" to "third"
