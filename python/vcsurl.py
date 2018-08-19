#!/usr/bin/env python3
import vim

from lib.utils import (get_project_dir_and_vcs, get_file_path,
                       get_url_mercurial, get_url_git)


def get_global_var(var_name, default=''):
    var_name = 'g:%s' % var_name
    if vim.eval("exists('%s')" % var_name) == '1':
        return vim.eval("eval('%s')" % var_name)
    return default


def get_vcs_line_url():
    w = vim.current.window
    b = vim.current.buffer
    pos = w.cursor
    line, col = pos
    fname = b.name
    project_dir, vcs_name = get_project_dir_and_vcs(fname)
    file_path = get_file_path(fname, project_dir)
    url = None
    if vcs_name == 'hg':
        url = get_url_mercurial(file_path, line)
    else:
        url = get_url_git(file_path, line)
    if url:
        register = get_global_var('vcsurl_register', '+')
        vim.command("let @%s='%s'" % (register, url))
        print('Success')
    else:
        print('Fail')
