import codecs
from os.path import dirname, join

from fictionary.model import Model

DATADIR = dirname(__file__)

_words = None


def get_words():
    global _words
    if _words is None:
        with codecs.open(join(DATADIR, "words.txt"), "r", encoding="utf-8") as fp:
            _words = set(w.strip() for w in fp.readlines())
    return _words


class LazyModel(object):
    def __init__(self, path):
        self._path = path
        self._model = None

    def __getattr__(self, name):
        if self._model is None:
            self._model = Model()
            with codecs.open(self._path, "r", encoding="utf-8") as fp:
                self._model.read(fp)
                self._model._words = get_words()
        return getattr(self._model, name)


all = LazyModel(join(DATADIR, "all.txt"))
american = LazyModel(join(DATADIR, "american.txt"))
british = LazyModel(join(DATADIR, "british.txt"))
