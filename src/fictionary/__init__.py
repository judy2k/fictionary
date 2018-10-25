#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A made-up word factory, following standard English word rules.
"""

from __future__ import print_function, unicode_literals

from collections import Counter
from glob import glob
import logging
from os import makedirs
from os.path import join, exists, dirname
import random
import shelve
import sys
import tempfile


LOG = logging.getLogger("fictionary")

APP_NAME = "fictionary"
DEFAULT_NUM_WORDS = 1
DEFAULT_MIN_LENGTH = 4

# Where to load the source ispell wordlists:
SRC_DATA_FILE_ROOT = dirname(__file__)

# Note: everywhere in this file that a string literal is being wrapped
# in str(), this is not useless, it does actually do something.
# As it turns out, it seems that shelve in Python 2.7 doesn't support
# Unicode shelf keys. And because we're using "import unicode_literals",
# all the literal shelf keys are effectively of the form u'key-name'.
# By wrapping the keys in str(), they become non-Unicode strings in
# Python 2, and they remain as Unicode in Python 3.
DICT_ALL_KEY = str("all")
DICT_BRITISH_KEY = str("british")
DICT_AMERICAN_KEY = str("american")

ISPELL_FILESETS = {
    DICT_ALL_KEY: glob(join(SRC_DATA_FILE_ROOT, "ispell_wordlist/*.*")),
    DICT_BRITISH_KEY: glob(join(SRC_DATA_FILE_ROOT, "ispell_wordlist/english.*"))
    + glob(join(SRC_DATA_FILE_ROOT, "ispell_wordlist/british.*")),
    DICT_AMERICAN_KEY: glob(join(SRC_DATA_FILE_ROOT, "ispell_wordlist/english.*"))
    + glob(join(SRC_DATA_FILE_ROOT, "ispell_wordlist/american.*")),
}

WORDLIST_KEY = str("wordlist")


class Markov(object):
    """ A markov chain, with 2-token tuples as keys.

    Values are implemented as Counter objects, providing a weighting for each
    successive token.
    """

    def __init__(self):
        self.data = {}

    def feed(self, tokens):
        """ Add a sequence of tokens for addition to the Markov model. """
        terms = [None, None] + list(tokens) + [None]
        for index in range(len(terms) - 2):
            pair = tuple(terms[index : index + 2])
            nxt = terms[index + 2]
            options = self.data.get(pair, None)
            if options is not None:
                options.update([nxt])
            else:
                options = RandomCounter([nxt])
                self.data[pair] = options

    def __getitem__(self, key):
        return self.data[key]

    def random_sequence(self, min_length=4, max_length=None, filter=None):
        """ Generate a random sequence from the Markov model.

        Any resulting sequences which are shorter than min_length (which
        defaults to 4) are filtered out.
        """
        if filter is None:
            filter = lambda x: x

        for _ in range(1000):
            result = list(self.random_sequence_generator())
            if (
                len(result) >= min_length
                and (max_length is None or len(result) <= max_length)
                and filter(result)
            ):
                LOG.debug(
                    "Result: %s (%d <= %d <= %r)",
                    result,
                    min_length,
                    len(result),
                    max_length,
                )
                return result
        raise Exception(
            "Couldn't find a valid word in 1000 iterations - "
            "it looks like something is wrong!"
        )

    def random_sequence_generator(self):
        """ A generator to provide a sequence from the Markov model. """
        key = (None, None)
        while True:
            next_token = self[key].random_choice()
            if not next_token:
                return
            else:
                yield next_token
                key = (key[1], next_token)


class RandomCounter(Counter):
    """ A Counter with extra methods for choosing random keys from the
    collection, accounting for weightings provided by the counter values.
    """

    def pick(self, i):
        """ Pick a key from Counter, using the key's count as a weighting.

        This function sorts counter contents in order of count, and uses each
        count as a range providing a weighting for the associated value. The
        parameter `i` provides an index into one of the ranges, and that
        count's associated key is returned.
        """
        total = 0
        for val, count in self.most_common():
            total += count
            if i < total:
                return val
        raise IndexError(
            "Value of i (%d) was greater than max index (%d)"
            % (i, sum(self.values()) - 1)
        )

    def random_choice(self, weighted=True):
        """ Obtain a randomly-chosen key from the counter.

        If weighted is True, the key returned is weighted by its associated
        count, so keys with a high count value should be chosen more
        frequently.  If weighted is False, the keys in counter are treated as
        a flat list, and each has the same probability of being chosen.
        """
        if weighted:
            return self.pick(random.randint(0, sum(self.values()) - 1))
        else:
            return random.choice(self.most_common())[0]


class DataFile(object):
    """
    A data file containing pickled markov chains and a dict of known words.
    """

    def __init__(self, path, filesets=None, refresh=False):
        self._shelf = None
        self.open_data_file(path, filesets or ISPELL_FILESETS, refresh)
        self.path = path

    def __getitem__(self, key):
        return self._shelf[str(key)]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """
        Close the open data filehandle.
        """
        if self._shelf:
            self._shelf.close()

    def generate_word_list(self, files):
        """
        Read through one or more wordlist files and generate a Markov object
        representing the words.

        ``files`` should be a sequence of file paths. Each file will be opened,
        and each line should contain a single word.  Words beginning with a
        capital letter or containing an apostrophe will be rejected. Each word
        is fed into a Markov object as a sequence of characters.
        """
        result = Markov()
        for path in files:
            for line in open(path):
                word = line.strip()
                if not line[0].isupper() and "'" not in word:
                    self._shelf[WORDLIST_KEY].add(word)
                    result.feed(word)
        self._shelf.sync()
        return result

    def open_data_file(self, data_file_path, filesets, force_refresh):
        """
        Open a fictionary data file, creating a new one if necessary, or if
        ``force_refresh`` is True.
        """
        containing_dir = dirname(data_file_path)
        if not exists(containing_dir):
            makedirs(containing_dir)
        if force_refresh:
            self._shelf = shelve.open(
                data_file_path, protocol=2, flag="n", writeback=True
            )
        else:
            self._shelf = shelve.open(
                data_file_path, protocol=2, flag="c", writeback=True
            )

        self.ensure_data(filesets)

    def ensure_data(self, filesets):
        """
        Create a new fictionary data file at ``data_file_path`` from the files
        listed in ``filesets``
        """
        self._shelf[WORDLIST_KEY] = set()
        for dictionary in [DICT_ALL_KEY, DICT_BRITISH_KEY, DICT_AMERICAN_KEY]:
            if not self._shelf.get(dictionary):
                LOG.debug("Started generating '%s' dictionary... " % dictionary)
                sys.stderr.flush()
                self._set_word_list(
                    dictionary, self.generate_word_list(filesets[dictionary])
                )
                LOG.debug("Finished generating '%s' dictionary." % dictionary)

    def _set_word_list(self, dictionary, word_list):
        self._shelf[dictionary] = word_list

    def is_real_word(self, word):
        """
        Checks the provided word to see if it's contained in the data file.
        """
        return word in self._shelf[WORDLIST_KEY]

    def get_random_word(self, dictionary, min_length, max_length):
        model = self[str(dictionary)]

        real_word_filter = lambda w: not self.is_real_word("".join(w))
        return str(
            "".join(model.random_sequence(min_length, max_length, real_word_filter))
        )


def get_temp_filepath():
    """Get the path to the dictionary database file.

    The Python 2 file is incompatible with the Python 3 file, so give
    it a different name.
    """
    data_file_root = tempfile.gettempdir()
    filename_version_suffix = "_py2" if sys.version_info[0] < 3 else ""
    filename = "{0}_dictionary{1}.dat".format(APP_NAME, filename_version_suffix)
    return join(data_file_root, filename)


def get_random_words(
    num_words=DEFAULT_NUM_WORDS,
    min_length=DEFAULT_MIN_LENGTH,
    max_length=None,
    dictionary=DICT_BRITISH_KEY,
    is_refresh=False,
    path=None,
):
    """Get a random sequence of fictionary words.

    Call this function to use fictionary from any other Python code.
    """
    path = path or get_temp_filepath()
    with DataFile(path, refresh=is_refresh) as shelf:
        return [
            shelf.get_random_word(
                dictionary, min_length=min_length, max_length=max_length
            )
            for _ in range(num_words)
        ]
