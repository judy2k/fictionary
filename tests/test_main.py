import mock

import fictionary.cli


def test_no_args():
    fictionary.cli.main([])


def test_min_below_max():
    assert fictionary.cli.main(["-m", "12", "-x", "10"]) == -1


def test_keyboard_interrupt():
    with mock.patch("fictionary.words", side_effect=KeyboardInterrupt):
        assert fictionary.cli.main([]) == 0
