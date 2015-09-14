import logging
import random
import re

import pytest

import fictionary


def test_weighted():
    random.seed(64)
    rc = fictionary.RandomCounter('aaaaaaaaaaaaab')
    assert [rc.random_choice() for i in range(6)] == list('aaaaab')

def test_unweighted():
    random.seed(64)
    rc = fictionary.RandomCounter('aaaaaaaaaaaaab')
    assert [rc.random_choice(weighted=False) for i in range(6)] == list('ababab')

def test_pick():
    rc = fictionary.RandomCounter('aaaaaaaaaaaaab')
    assert rc.pick(0) == 'a'
    assert rc.pick(12) == 'a'
    assert rc.pick(13) == 'b'

def test_pick():
    rc = fictionary.RandomCounter('aaaaaaaaaaaaab')
    with pytest.raises(IndexError):
        rc.pick(14)
