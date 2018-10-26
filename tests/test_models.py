import codecs
import io
import json
import logging
from os.path import dirname, join
import fictionary.models

logging.basicConfig(level=logging.DEBUG)

LOG = logging.getLogger("fictionary.tests")


def test_load_model():
    path = join(dirname(fictionary.models.__file__), "all.txt")
    m = fictionary.model.Model()
    with codecs.open(path, "r", encoding="utf-8") as fp:
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


def test_model_feed():
    m = fictionary.model.Model()
    m.feed("table")
    m.feed("babel")
    assert m.is_real_word("table")
    assert "tabel" in {m.random_word(5, 5) for _ in range(100)}


def test_model_to_json():
    m = fictionary.model.Model()
    m.feed("table")
    j = m.to_json()
    assert j["ver"] == 1
    assert j["markov"] == {
        ",": {"t": 1},
        ",t": {"a": 1},
        "t,a": {"b": 1},
        "a,b": {"l": 1},
        "b,l": {"e": 1},
        "l,e": {"": 1},
    }


def test_model_write():
    fp = io.StringIO()
    m = fictionary.model.Model()
    m.feed("table")
    m.write(fp)

    j = json.loads(fp.getvalue())
    assert j["ver"] == 1
    assert j["markov"] == {
        ",": {"t": 1},
        ",t": {"a": 1},
        "t,a": {"b": 1},
        "a,b": {"l": 1},
        "b,l": {"e": 1},
        "l,e": {"": 1},
    }
