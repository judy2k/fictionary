Fictionary
==========

.. image:: https://travis-ci.com/judy2k/fictionary.svg?branch=master
    :target: https://travis-ci.com/judy2k/fictionary
.. image:: https://coveralls.io/repos/github/judy2k/fictionary/badge.svg?branch=master
    :target: https://coveralls.io/github/judy2k/fictionary?branch=master
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

Generate made-up words following the patterns used by real English words.

Using Fictionary
----------------

Install with::

    pip install --upgrade fictionary

You can learn how to use fictionary as a command-line tool by running `fictionary -h`::

    usage: fictionary [-h] [-v] [-c COUNT] [-m LENGTH] [-x LENGTH]
                      [-d {all,american,british}]

    A made-up word factory, following standard English word rules.

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         Be verbose.
      -c COUNT, --count COUNT
                            The number of words to make_model.
      -m LENGTH, --min-length LENGTH
                            Only make_model words of LENGTH chars or longer.
      -x LENGTH, --max-length LENGTH
                            Only make_model words of LENGTH chars or shorter.
      -d {all,american,british}, --dictionary {all,american,british}
                            The dictionary rules to follow: american, british, or
                            all

And you can also use it as a library:

    >>> import fictionary

    >>> fictionary.word()
    'regagreagised'

And if you want to create your own models::

    # Create a model and add a couple of words to it:
    m = fictionary.Model()
    m.feed('table')
    m.feed('babel')

    # Now we can generate words! (This model is capable of only 2 fictional words)
    print(m.random_word(5, 5)) # tabel
    print(m.random_word(5, 5)) # bable

    # If you're building a model with *lots* of words, generating the model can be slow, so
    # you can save the generated model to a json file:
    with open('my-fictionary-dict.json', 'w', encoding='utf-8') as fp:
        m.write(fp)

    # And then later you'll want to read it in with this:
    # (You still need to supply a list of 'real' words, for collision detection)
    new_model = fictionary.Model(words=['table', 'babel'])
    with open('my-fictionary-dict.json', 'r', encoding='utf-8') as fp:
        new_model.read(fp)

Why???
------

Why not? It is particularly good for generating memorable yet reasonable
length passwords, although I'm not sure how secure those passwords would be
given that they follow well-defined patterns. One day I might sit down and
work it out.

What Should I Expect To See
---------------------------

The results are random, but you should see something like the following::

    $ fictionary.py --count 20 --min-length 5
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

When it runs, fictionary loads a data structure
called a Markov chain, which represents the patterns of letters found in the
words in the dictionary (e.g. The most common first-letter is 's'. The most common letter
following 's' at the start of a word is 't' etc.)

Once fictionary understands the patterns of letters used in words in the
English language, it can use these rules to generate new, nonsense words that
look like English words, but aren't. It's so easy for the Markov chain to
accidentally generate a real English word that we have to check each generated
word against a dictionary to make sure it isn't.

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
Optimize Long Words
    Make word-generator bail out as soon as max-length is encountered.
