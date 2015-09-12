
import fictionary


def test_predictable():
    markov = fictionary.Markov()
    markov.feed("abcde")
    assert ''.join(markov.random_sequence(5, 5)) == "abcde"

