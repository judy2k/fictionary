#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A made-up word factory, following standard English word rules.
"""

from __future__ import print_function, unicode_literals

from collections import Counter
from glob import glob
import importlib
import logging
from os import makedirs
from os.path import join, exists, dirname
import random
import sys

from io import StringIO


LOG = logging.getLogger("fictionary")

APP_NAME = "fictionary"
DEFAULT_NUM_WORDS = 1
DEFAULT_MIN_LENGTH = 4
DEFAULT_MAX_LENGTH = None

DICT_ALL_KEY = "all"
DICT_BRITISH_KEY = "british"
DICT_AMERICAN_KEY = "american"


class Model(object):
    def __init__(self, markov_data=None, words=None):
        self._markov = Markov(markov_data) if markov_data is not None else Markov()
        self._words = words if words is not None else set()

    def feed(self, word):
        self._words.add(word)
        self._markov.feed(word)

    def is_real_word(self, word):
        return word in self._words

    def random_word(self, min_length=DEFAULT_MIN_LENGTH, max_length=DEFAULT_MAX_LENGTH):
        real_word_filter = lambda w: not self.is_real_word("".join(w))
        return str(
            "".join(
                self._markov.random_sequence(min_length, max_length, real_word_filter)
            )
        )

    def _code_repl(self):
        result = StringIO()
        result.write(
            "Model(markov_data={markov_data!r})".format(markov_data=self._markov.data)
        )
        return result.getvalue()


class Markov(object):
    """ A markov chain, with 2-token tuples as keys.

    Values are implemented as Counter objects, providing a weighting for each
    successive token.
    """

    def __init__(self, data=None):
        self.data = data if data is not None else {}

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

    def _raw_data(self):
        return {k: dict(v) for k, v in self.data.items()}


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


def get_random_words(
    num_words=DEFAULT_NUM_WORDS,
    min_length=DEFAULT_MIN_LENGTH,
    max_length=DEFAULT_MAX_LENGTH,
    dictionary=DICT_BRITISH_KEY,
):
    """Get a random sequence of fictionary words.

    Call this function to use fictionary from any other Python code.
    """
    mod = importlib.import_module("fictionary.models." + dictionary)
    return [mod.model.random_word() for _ in range(num_words)]
