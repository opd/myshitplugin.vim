#!/usr/bin/env python3
import hashlib
import os
import os.path
from pathlib import Path
import vim

from lib.utils import (get_project_dir_and_vcs, get_file_path,
                       get_url_mercurial, get_url_git, move_word)


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


def get_string_hash(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def per_project_viminfo():
    # TODO disable function by default
    # TODO custom viminfo directory
    fname = vim.eval("getcwd()")
    project_dir, vcs_name = get_project_dir_and_vcs(fname)
    file_name = 'root'
    if vcs_name:
        file_name = get_string_hash(project_dir)
    viminfo_dir = '.viminfos'
    viminfo_dir = os.path.join(str(Path.home()), viminfo_dir)
    path = os.path.join(viminfo_dir, file_name)
    new_viminfo = False
    if not os.path.isfile(path):
        new_viminfo = True
        if not os.path.isdir(viminfo_dir):
            os.mkdir(viminfo_dir)
    cmd = "set viminfo='10,\\\"100,:20,%%,n%s" % path
    vim.command(cmd)
    if new_viminfo:
        vim.command("wv")
    vim.command("rv")


def move_text(left_to_right_direction=False):
    b = vim.current.buffer
    vim.command("echom 'move_text'")
    w = vim.current.window
    b = vim.current.buffer
    pos = w.cursor
    line_number, col = pos
    # prev_line = b[line_number - 1]
    line = b[line_number - 1]
    # next_line = b[line_number + 1]
    res = move_word('', line, '', col, left_to_right_direction)
    if res:
        new_line = res['current_line']
        new_col = res['col']
        pos = (line_number, new_col)
        w.cursor = pos
        b[line_number - 1] = new_line


def capture():
    begin = vim.eval('getpos("\'<")')
    end = vim.eval('getpos("\'>")')
    directory = os.path.dirname(os.path.abspath(__file__))
    script = os.path.join(directory, 'capture.py')
    fname = vim.eval("expand('%:p')")
    params = {
        "script": script,
        "filename": fname,
        "from": begin[1],
        "to": end[1],
    }
    cmd = "call system('%(script)s %(filename)s %(from)s %(to)s> " % params
    cmd += "/dev/null 2>&1 &')"
    vim.command(cmd)
