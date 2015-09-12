
import fictionary


def test_predictable():
    markov = fictionary.Markov()
    markov.feed("abcde")
    assert ''.join(markov.random_sequence(5, 5)) == "abcde"


def test_impossible():
    markov = fictionary.Markov()
    markov.feed("abcdefghi")
    assert ''.join(markov.random_sequence(5, 5)) == 'abcde'
