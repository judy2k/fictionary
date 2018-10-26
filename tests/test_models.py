from glob import glob
from os.path import dirname, join, exists

import pytest
import mock

import fictionary

import logging

logging.basicConfig(level=logging.DEBUG)

LOG = logging.getLogger("fictionary.tests")


def test_getitem():
    import fictionary.models.american as am

    print(am.model._markov.data[("x", "u")])
    assert set(am.model._markov.data[("x", "u")].keys()) == set(
        ["a", "r", "l", "s", "d", "b", "v", "p", "o", "m", "t"]
    )


def test_is_real_word():
    import fictionary.models.american as am

    assert am.model.is_real_word("xxxxxx") is False
    assert am.model.is_real_word("beclamour") is True
