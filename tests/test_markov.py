import logging
import random
import re

import fictionary.markov
import pytest

import fictionary


def test_predictable():
    markov = fictionary.markov.Markov()
    markov.feed("abcde")
    assert "".join(markov.random_sequence(5, 5)) == "abcde"


def test_multiple_options():
    random.seed(64)
    logging.getLogger().setLevel(logging.DEBUG)
    markov = fictionary.markov.Markov()
    markov.feed("abccde")
    markov.feed("cccde")
    generated = "".join(markov.random_sequence(7))
    assert re.match(r"abc+de", generated)


def test_impossible():
    markov = fictionary.markov.Markov()
    markov.feed("abcdefghi")
    with pytest.raises(Exception):
        markov.random_sequence(5, 5)
