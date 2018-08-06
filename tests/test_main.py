import logging

import mock
import pytest

import fictionary

def test_no_args():
    with mock.patch('fictionary.DataFile', autospec=True) as df:
        fictionary.main([])
        assert df.called
        args, kwargs = df.call_args
        assert kwargs['refresh'] is False


def test_refresh():
    with mock.patch('fictionary.DataFile', autospec=True) as df:
        result = fictionary.main(['--refresh'])
        assert df.called
        args, kwargs = df.call_args
        assert kwargs['refresh'] is True
        assert result == 0


def test_min_below_max():
    with mock.patch('fictionary.DataFile', autospec=True) as df:
        assert fictionary.main(['-m', '12', '-x', '10']) == -1
        assert not df.called


def test_keyboard_interrupt():
    with mock.patch('fictionary.DataFile', side_effect=KeyboardInterrupt):
        assert fictionary.main([]) == 0


def test_verbosity():
    with mock.patch('fictionary.DataFile', side_effect=KeyboardInterrupt):
        with mock.patch('fictionary.LOG') as fictionary_logger:
            fictionary.main([])
            fictionary_logger.setLevel.assert_called_once_with(logging.WARNING)

        with mock.patch('fictionary.LOG') as fictionary_logger:
            fictionary.main(['-v'])
            fictionary_logger.setLevel.assert_called_once_with(logging.DEBUG)
