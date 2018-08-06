from unittest import mock
import pytest

import fictionary


def test_no_args():
    with mock.patch('fictionary.DataFile', autospec=True) as df:
        random_words = fictionary.get_random_words()
        assert len(random_words) == fictionary.DEFAULT_NUM_WORDS


def test_num_words():
    with mock.patch('fictionary.DataFile', autospec=True) as df:
        random_words = fictionary.get_random_words(num_words=42)
        assert len(random_words) == 42
