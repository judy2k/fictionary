import logging
from os.path import dirname, join

logging.basicConfig(level=logging.DEBUG)

LOG = logging.getLogger("fictionary.tests")

import fictionary.models


def test_load_model():
    path = join(dirname(fictionary.models.__file__), "all.txt")
    m = fictionary.model.Model()
    with open(path, "r", encoding="utf-8") as fp:
        m.read(fp)
    assert m.random_word() is not None


def test_lazy_model():
    path = join(dirname(fictionary.models.__file__), "all.txt")
    m = fictionary.models.LazyModel(path)
    assert m.random_word() is not None


def test_getitem():
    am = fictionary.models.american
    assert set(am._markov.data[("x", "u")].keys()) == set(
        ["a", "r", "l", "s", "d", "b", "v", "p", "o", "m", "t"]
    )


def test_is_real_word():
    am = fictionary.models.american

    assert am.is_real_word("xxxxxx") is False
    assert am.is_real_word("beclamour") is True
