import json

from fictionary.markov import Markov

DEFAULT_MIN_LENGTH = 4
DEFAULT_MAX_LENGTH = None

SUPPORTED_FILE_VER = 1


class FileVersionError(Exception):
    pass


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

    def to_json(self):
        return {"ver": 1, "markov": self._markov.to_json()}

    def read(self, fp):
        """
        :raises FileVersionError: if the version of the saved file is not supported
        :param fp:
        :return:
        """
        j = json.load(fp)
        if j["ver"] != 1:
            raise FileVersionError(
                "Attempt to read file of version {ver}, but this version of fictionary can only read version {supported}".format(
                    ver=j["ver"], supported=SUPPORTED_FILE_VER
                )
            )
        else:
            self._markov = Markov.from_json(j["markov"])

    def write(self, fp):
        json.dump(self.to_json(), fp)
