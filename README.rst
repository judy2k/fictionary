Fictionary
==========

Generate made-up words following the patterns used by real English words.

How it Works
------------

The first time it runs, fictionary loads a word database into a data structure
called a Markov chain, which represents the patterns of letters found in the
words (e.g. The most common first-letter is 's'. The most common letter
following 's' at the start of a word is 't' etc.)

Once fictionary understands the patterns of letters used in words in the
English language, it can use these rules to generate new, nonsense words that
look like English words, but (probably) aren't.

Why???
------

Why not? It is particularly good for generating memorable yet reasonable
length passwords, although I'm not sure how secure those passwords would be
given that they follow well-defined patterns. One day I might sit down and
work it out.

Using Fictionary
----------------

Fictionary doesn't have any sort of installer at the moment. If you have
python installed, just clone this repository, and run
``fictionary.py --help``. This should print out something like the
following::

    usage: fictionary.py [-h] [-v] [-c COUNT] [-m MIN]

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Be verbose.
      -c COUNT, --count COUNT
                            The number of words to generate.
      -m MIN, --min-length MIN
                            Only generate words of MIN length or longer.