import logging
import random
from collections import Counter

LOG = logging.getLogger("fictionary.markov")


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
            "Couldn't find a valid word in 1000 iterations - it looks like something is wrong!"
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

    @staticmethod
    def _to_keystring(key):
        return ",".join(c if c is not None else "" for c in key)

    @staticmethod
    def _from_keystring(key):
        return tuple(c if c != "" else None for c in key.split(","))

    def to_json(self):
        return {self._to_keystring(k): v.to_json() for k, v in self.data.items()}

    @classmethod
    def from_json(cls, data):
        return cls(
            {
                cls._from_keystring(k): RandomCounter.from_json(v)
                for k, v in data.items()
            }
        )


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

    @staticmethod
    def _to_keystring(k):
        return k if k is not None else ""

    @staticmethod
    def _from_keystring(k):
        return k if k != "" else None

    def to_json(self):
        return {self._to_keystring(k): v for k, v in self.items()}

    @classmethod
    def from_json(cls, j):
        return cls({cls._from_keystring(k): v for k, v in j.items()})
