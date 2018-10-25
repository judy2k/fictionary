import mock

import fictionary


def test_no_args():
    with mock.patch("fictionary.DataFile", autospec=True) as df:
        fictionary.cli.main([])
        assert df.called
        args, kwargs = df.call_args
        assert kwargs["refresh"] is False


def test_refresh():
    with mock.patch("fictionary.DataFile", autospec=True) as df:
        result = fictionary.cli.main(["--refresh"])
        assert df.called
        args, kwargs = df.call_args
        assert kwargs["refresh"] is True
        assert result == 0


def test_min_below_max():
    with mock.patch("fictionary.DataFile", autospec=True) as df:
        assert fictionary.cli.main(["-m", "12", "-x", "10"]) == -1
        assert not df.called


def test_keyboard_interrupt():
    with mock.patch("fictionary.DataFile", side_effect=KeyboardInterrupt):
        assert fictionary.cli.main([]) == 0
