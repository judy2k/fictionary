#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" A made-up word factory, following standard English word rules.
"""

from __future__ import print_function, unicode_literals

import importlib
import logging

from fictionary.model import DEFAULT_MIN_LENGTH, DEFAULT_MAX_LENGTH
import fictionary.models

APP_NAME = "fictionary"
DEFAULT_NUM_WORDS = 1

DICT_ALL_KEY = "all"
DICT_BRITISH_KEY = "british"
DICT_AMERICAN_KEY = "american"

LOG = logging.getLogger("fictionary")


def get_random_words(
    num_words=DEFAULT_NUM_WORDS,
    min_length=DEFAULT_MIN_LENGTH,
    max_length=DEFAULT_MAX_LENGTH,
    dictionary=DICT_BRITISH_KEY,
):
    """Get a random sequence of fictionary words.

    Call this function to use fictionary from any other Python code.
    """
    mod = getattr(fictionary.models, dictionary)
    return [
        mod.random_word(min_length=min_length, max_length=max_length)
        for _ in range(num_words)
    ]
