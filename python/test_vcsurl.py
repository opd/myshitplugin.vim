from unittest import mock

import pytest

from lib.utils import get_url_git, get_url_mercurial


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
    (b'git@github.com:coder/myblog.git',
     'https://bitbucket.org/supercoders/myblog/src/master'
     '/backend/apps/myblog/models.py#lines-123'),
    (b'https://github.com/supercoders/myblog.git',
     'https://github.com/supercoders/myblog.git')
])
def test_get_url_git(monkeypatch, case):
    path, url = case
    shell_mock = mock.Mock(return_value=path)
    monkeypatch.setattr('lib.utils.run_shell_command', shell_mock)
    file_path = '/backend/apps/myblog/models.py'
    line = 123

    assert get_url_git(file_path, line) == url
