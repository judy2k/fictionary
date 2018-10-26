#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A made-up word factory, following standard English word rules.
"""

from __future__ import print_function, unicode_literals

import importlib
import logging

from io import StringIO

from fictionary.markov import Markov

APP_NAME = "fictionary"
DEFAULT_NUM_WORDS = 1
DEFAULT_MIN_LENGTH = 4
DEFAULT_MAX_LENGTH = None

DICT_ALL_KEY = "all"
DICT_BRITISH_KEY = "british"
DICT_AMERICAN_KEY = "american"

LOG = logging.getLogger("fictionary")


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
