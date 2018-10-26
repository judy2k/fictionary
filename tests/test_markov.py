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


def test_markov_to_json():
    markov = fictionary.markov.Markov()
    markov.feed("abc")
    assert markov.to_json() == {
        ",": {"a": 1},
        ",a": {"b": 1},
        "a,b": {"c": 1},
        "b,c": {"": 1},
    }


def test_markov_from_json():
    markov = fictionary.markov.Markov.from_json(
        {",": {"a": 1}, ",a": {"b": 1}, "a,b": {"c": 1}, "b,c": {"": 1}}
    )
    assert markov.random_sequence(min_length=1) == list("abc")


def test_randomcounter_to_json():
    rc = fictionary.markov.RandomCounter({None: 12, "a": 42})
    assert rc.to_json() == {"": 12, "a": 42}


def test_randomcounter_markov_from_json():
    rc = fictionary.markov.RandomCounter.from_json({"": 12, "a": 42})
    assert rc[None] == 12
    assert rc["a"] == 42
