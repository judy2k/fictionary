Fictionary
==========

Generate made-up words following the patterns used by real English words.

Using Fictionary
----------------

Fictionary doesn't have any sort of installer at the moment. If you have
python installed, just clone this repository, and run
``fictionary.py --help``. This should print out something like the
following::

    usage: fictionary.py [-h] [-v] [-c COUNT] [-m LENGTH] [-x LENGTH] [--refresh]
                         [-d DICTIONARY]

    A made-up word factory, following standard English word rules.

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Be verbose.
      -c COUNT, --count COUNT
                            The number of words to generate.
      -m LENGTH, --min-length LENGTH
                            Only generate words of LENGTH chars or longer.
      -x LENGTH, --max-length LENGTH
                            Only generate words of LENGTH chars or shorter.
      --refresh             Re-create the data file from the word-lists.
      -d DICTIONARY, --dictionary DICTIONARY
                            The dictionary rules to follow: american,british, or
                            all

**Note:** `Click <http://click.pocoo.org/>`_ is an optional dependency
of Fictionary. It can be installed with a quick ``pip install click``.
If it's installed, then the generated dictionary file will be saved in a
persistent location per Click's ``get_app_dir()``. Otherwise, the
generated dictionary file will be saved to your system's default temp
directory, where it may get lost between app or system restarts (the
file gets re-generated automatically if it's not found, so it's no big
deal, but it's a bit slow each time it re-generates).

Why???
------

Why not? It is particularly good for generating memorable yet reasonable
length passwords, although I'm not sure how secure those passwords would be
given that they follow well-defined patterns. One day I might sit down and
work it out.

What Should I Expect To See
---------------------------

The results are random, but you should see something like the following::

    $ fictionary.py -c 20 -m 5
    prodybating
    awbalemisfrewhic
    billars
    rotous
    fratorgater
    incens
    cradpantle
    gatinspon
    intneshemblary
    clumake
    pladrachoppedally
    fuledi
    pheable
    frilita
    sederels
    hippostaligarupyrrelised
    haridisuppechooge
    turefurnic
    butermel
    amblier

How it Works
------------

The first time it runs, fictionary loads a word database into a data structure
called a Markov chain, which represents the patterns of letters found in the
words (e.g. The most common first-letter is 's'. The most common letter
following 's' at the start of a word is 't' etc.)

Once fictionary understands the patterns of letters used in words in the
English language, it can use these rules to generate new, nonsense words that
look like English words, but (probably) aren't.

Releasing
---------

These are notes for me, as is probably obvious:

* **Check the README**
* `bumpversion`
* `python setup.py sdist bdist_wheel`
* `twine upload dist/*.*`

To Do
-----

The following is my to-do list for this project:

Allow Valid Words
    Add a flag to turn off 'real-word' validation.
Word Generation Rollback
    Rejecting words that are too long or short is reasonably expensive. I may
    refactor this to rollback and remake choices until a valid 'word' is
    reached. Or I may find something better to do with my time.
Auto-Refresh
    Automatically recreate the data file if the source files change.
Data-File Optimisation
    Generate the markov chains in parallel, so files don't have to be re-read.
Optimize Long Words
    Make word-generator bail out as soon as max-length is encountered.
