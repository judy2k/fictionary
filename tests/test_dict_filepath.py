import mock

import fictionary


def test_py2():
    with mock.patch("sys.version_info", [2]):
        path = fictionary.get_temp_filepath()
        assert "_py2" in path


def test_py3():
    with mock.patch("sys.version_info", [3]):
        path = fictionary.get_temp_filepath()
        assert "_py2" not in path
