import os
import re
import subprocess


def get_project_dir_and_vcs(fname):
    orig_path = project_path = fname
    while True:
        for svn, folder in [('hg', '.hg'), ('git', '.git')]:
            path = os.path.join(project_path, folder)
            if os.path.exists(path) and os.path.isdir(path):
                return project_path, svn
        project_path = os.path.dirname(project_path)
        if project_path == '/':
            return orig_path, None


def run_shell_command(arr):
    result = subprocess.check_output(arr)
    return result


def get_url_mercurial(file_path, line):
    default_path = run_shell_command(['hg', 'path', 'default'])
    default_path = default_path.decode()
    default_path = default_path.replace('\n', '')

    domain = r'(?P<domain>bitbucket\.org)'
    team = r'(?P<team>[^/]+)'
    project = r'(?P<project>[^/]+)'
    username = r'(?P<username>[^@]+)'

    bb_ssh_pattern = r'^ssh://hg@{domain}/{team}/{project}$'
    bb_https_pattern = r'^https://{username}@{domain}/{team}/{project}$'

    patterns = [bb_ssh_pattern, bb_https_pattern]
    result = None
    for pattern in patterns:
        pattern = pattern.format(domain=domain, team=team,
                                 project=project, username=username)
        m = re.match(pattern, default_path)
        if m:
            result = m.groupdict()
            break
    if result:
        domain = result['domain']
        team = result['team']
        project = result['project']
        if domain == 'bitbucket.org':
            url = 'https://{domain}/{team}/{project}/src/default'
            url = url.format(domain=domain, team=team, project=project)
            url += file_path
            url += '#lines-{line}'.format(line=line)
            return url


def get_url_git(file_path, line):
    # git config --get remote.origin.url
    default_path = run_shell_command(['git', 'config', '--get',
                                      'remote.origin.url'])
    default_path = default_path.decode()
    default_path = default_path.replace('\n', '')

    domain = r'(?P<domain>bitbucket\.org|github\.com)'
    team = r'(?P<team>[^/]+)'
    project = r'(?P<project>[^/]+)'
    username = r'(?P<username>[^@]+)'

    # git@bitbucket.org:team/project.git
    bb_ssh_pattern = r'^git@{domain}:{team}/{project}[.]git$'
    # not tested
    # https://username@bitbucket.org/team/project.git
    bb_https_pattern = r'^https://{username}@{domain}/{team}/{project}[.]git$'
    # https://github.com/opd/vcsurl.vim.git
    gh_https_pattern = r'^https://{domain}/{team}/{project}[.]git$'
    # git@github.com:opd/vcsurl.vim.git
    gh_ssh_pattern = r'^git@{domain}:{team}/{project}[.]git$'  # duplicate bb

    patterns = [bb_ssh_pattern, bb_https_pattern, gh_https_pattern,
                gh_ssh_pattern]
    result = None
    for pattern in patterns:
        pattern = pattern.format(domain=domain, team=team,
                                 project=project, username=username)
        m = re.match(pattern, default_path)
        if m:
            result = m.groupdict()
            break
    if result:
        domain = result['domain']
        team = result['team']
        project = result['project']
        # https://bitbucket.org/team/project/src/master/path_to_file#lines-12
        if domain == 'bitbucket.org':
            url = 'https://{domain}/{team}/{project}/src/master'
            url = url.format(domain=domain, team=team, project=project)
            url += file_path
            url += '#lines-{line}'.format(line=line)
            return url
        # https://github.com/opd/vcsurl.vim/blob/master/python/vcsurl.py#L8
        elif domain == 'github.com':
            url = 'https://{domain}/{team}/{project}/blob/master'
            url = url.format(domain=domain, team=team, project=project)
            url += file_path
            url += '#L{line}'.format(line=line)
            return url


def get_file_path(full_path, project_dir):
    return full_path[len(project_dir):]
