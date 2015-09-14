from glob import glob
from os.path import dirname, join, exists
import random
import re

import pytest
import mock

import fictionary


SRC_DATA_FILE_ROOT = join(dirname(__file__), "data")
ISPELL_FILESETS = {
    'all': glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/*.*')),
    'british': glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/english.*')) +
    glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/british.*')),
    'american': glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/english.*')) +
    glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/american.*')),
}


@pytest.fixture
def datafile(tmpdir):
    path = tmpdir.join('fictionary_temporary.data')
    return fictionary.DataFile(str(path), filesets=ISPELL_FILESETS)


def test_context(datafile):
    with mock.patch.object(datafile, '_shelf') as shelf:
        with datafile as ctx:
            assert datafile is ctx
        assert shelf.close.called_once_with()


def test_getitem(datafile):
    assert datafile['american'][('x', 'u')].keys() == ['a']


def test_open_existing_file(datafile):
    path = datafile.path

    before = datafile['british'][('a', 'b')]

    datafile.close()

    df = fictionary.DataFile(path)
    assert before == df['british'][('a', 'b')]


def test_is_real_word(datafile):
    assert datafile.is_real_word('xxxxxx') == False
    assert datafile.is_real_word('beclamour') == True


def test_create_intermediate_dirs(tmpdir):
    with mock.patch('fictionary.makedirs') as makedir_mock, \
            mock.patch('fictionary.shelve'):

        path = tmpdir.join('nonexistant/fictionary_temporary.data')
        fictionary.DataFile(str(path), filesets=ISPELL_FILESETS)
        makedir_mock.assert_called_once_with(path.dirname)


def test_refresh_true(datafile):
    datafile.close()
    assert exists(datafile.path)
    with mock.patch.object(fictionary.DataFile, 'generate_data_file') as gdf:
        fictionary.DataFile(datafile.path, filesets=ISPELL_FILESETS, refresh=True)
        gdf.assert_called_once_with(datafile.path, ISPELL_FILESETS)
