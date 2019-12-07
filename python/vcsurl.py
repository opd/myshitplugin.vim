#!/usr/bin/env python3
import hashlib
import itertools as it
import os
import os.path
from pathlib import Path
import re
import vim

from lib.utils import (get_project_dir_and_vcs, get_file_path,
                       get_url_mercurial, get_url_git)


def create_pattern(pattern, all_occurences=False):
    # TODO filter letters
    pattern = list(pattern)
    result = ".*".join(pattern)
    if not all_occurences:
        result = "^.*%s.*$" % result

    return re.compile(result)


def find_occurences(line, pattern):
    if not pattern:
        return []
    char = pattern[0]
    result = []
    for i, c in enumerate(line):
        if c == char:
            if len(pattern) == 1:
                result.append([0] * i + [1] + [0] * (len(line) - i - 1))
                continue
            recur_results = find_occurences(line[(i+1):], pattern[1:])
            if recur_results:
                begin = [0] * i + [1]
                for res in recur_results:
                    result.append(begin + res)
    return result


def distance_rate(occurence):
    data = list(i for i, x in enumerate(occurence) if x)
    data = (b - a for a, b in zip(data, data[1:]))
    data = (1 / x for x in data)
    return sum(data)


def _get_weight(line, occurence):
    return distance_rate(occurence)


def get_weight(line, pattern):
    occurences = find_occurences(line, pattern)
    return max([_get_weight(line, occurence) for occurence in occurences])


def match_func(lines, str_, count):
    pattern = create_pattern(str_)
    result = []
    for line in lines:
        m = pattern.match(line)
        if m:
            weight = get_weight(line, str_)
            result.append((line, weight))
    result = sorted(result, reverse=True, key=lambda x: x[1])
    result = (x[0] for x in result)
    return list(it.islice(result, 0, count))


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


def _custom_match(
    items, str_, limit, mmode, ispath, crfile, regex
):
    return items


def custom_match():
    items = vim.eval('a:items')
    str_ = vim.eval('a:str')
    limit = vim.eval('a:limit')
    mmode = vim.eval('a:mmode')
    ispath = vim.eval('a:ispath')
    crfile = vim.eval('a:crfile')
    regex = vim.eval('a:regex')
    items = match_func(
        items, str_, int(limit)
    )
    if False:
        # Dump data
        d = {
            'items': items,
            'str': str_,
            'limit': limit,
            'mmode': mmode,
            'ispath': ispath,
            'crfile': crfile,
            'regex': regex,
        }
        import json
        d = json.dumps(d)
        with open('/tmp/vim_item.py', 'w') as f:
            f.write(d)
    vim.command('let ret_val = %s' % items)
