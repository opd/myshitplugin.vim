from unittest import mock

import pytest

from lib.utils import get_url_git, get_url_mercurial, move_word
from lib import utils


@pytest.mark.parametrize('case', [
    (b'ssh://hg@bitbucket.org/supercoders/myblog\n',
     'https://bitbucket.org/supercoders/myblog/src/default'
     '/backend/apps/myblog/models.py#lines-123'),
    (b'https://coder@bitbucket.org/supercoders/myblog\n',
     'https://bitbucket.org/supercoders/myblog/src/default'
     '/backend/apps/myblog/models.py#lines-123'),
])
def test_get_url_mercurial(monkeypatch, case):
    path, url = case
    shell_mock = mock.Mock(return_value=path)
    monkeypatch.setattr('lib.utils.run_shell_command', shell_mock)
    file_path = '/backend/apps/myblog/models.py'
    line = 123
    assert get_url_mercurial(file_path, line) == url


@pytest.mark.parametrize('case', [
    (b'git@bitbucket.org:supercoders/myblog.git',
     'https://bitbucket.org/supercoders/myblog/src/master'
     '/backend/apps/myblog/models.py#lines-123'),
    (b'https://coder@bitbucket.org/supercoders/myblog.git',
     'https://bitbucket.org/supercoders/myblog/src/master'
     '/backend/apps/myblog/models.py#lines-123'),
    # (b'git@github.com:coder/myblog.git',
    #  'https://bitbucket.org/supercoders/myblog/src/master'
    #  '/backend/apps/myblog/models.py#lines-123'),
    # (b'https://github.com/supercoders/myblog.git',
    #  'https://github.com/supercoders/myblog.git')
])
def test_get_url_git(monkeypatch, case):
    path, url = case
    shell_mock = mock.Mock(return_value=path)
    monkeypatch.setattr('lib.utils.run_shell_command', shell_mock)
    file_path = '/backend/apps/myblog/models.py'
    line = 123

    assert get_url_git(file_path, line) == url


def test_get_word_begin():
    #    0123456789012345
    s = "asdf  asdf  asdf"
    assert utils.get_word_begin(s, 3) == 0
    assert utils.get_word_begin(s, 8) == 6
    assert utils.get_word_begin(s, 15) == 12


def test_get_word_bound():
    #              1         2         3
    #    0123456789012345678901234567890123456789
    s = "asdf(a, b, t(c)),  asdf,  asdf, s='a'"
    assert utils.get_word_bounds(s, 19) == (19, 22)
    assert utils.get_word_bounds(s, 0) == (0, 15)
    assert utils.get_word_bounds(s, 32) == (32, 36)


def test_split_str():
    #    0         1         2
    #    01234567890123456789012345
    s = "before first, second after"
    "before ", "first", ", ", "second", " after " == \
        utils.split_str(s, 7, 11, 14, 19)


def test_move_word():
    #              1         2
    #    0123456789012345678901234567890
    s = "   second, first = first, second"
    result = move_word('', s, '', 5, True)
    assert result['current_line'] == \
        "   first, second = first, second"
    assert result['col'] == 12
    #              1         2
    #    0123456789012345678901234567890
    s = "   s(c, o=1), first(1, 2, 3) = first, second"
    result = move_word('', s, '', 3, True)
    assert result['current_line'] == \
        "   first(1, 2, 3), s(c, o=1) = first, second"
    assert result['col'] == 19
