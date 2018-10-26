import mock

import fictionary


def test_no_args():
    random_words = fictionary.get_random_words()
    assert len(random_words) == fictionary.DEFAULT_NUM_WORDS


def test_num_words():
    random_words = fictionary.get_random_words(num_words=42)
    assert len(random_words) == 42
