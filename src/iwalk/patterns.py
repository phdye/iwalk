# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import errno

from iwalk.vendor.pathspec import PathSpec
from iwalk.vendor.pathspec.patterns.gitwildmatch import GitWildMatchPattern

IGNORE_FILENAMES = ['.gitignore', '.dockerignore', '.ignore']


class GlobalIgnoreLoadError(Exception):
    """Generic failure to load global ignore patterns."""
    pass


class GitCommandNotFound(GlobalIgnoreLoadError):
    """Raised when the Git command is not found in the system path.

    This usually means Git is not installed or not accessible from the current shell.
    Callers should catch this to fall back or alert the user appropriately.
    """
    pass


class GitConfigMissingError(GlobalIgnoreLoadError):
    """Raised when Git is installed but the 'core.excludesFile' config is missing or unreadable.

    This could mean the user has not set a global ignore file, or there is a config access issue.
    """
    pass


def read_patterns_from_file(filepath):
    if not os.path.isfile(filepath):
        return []
    with open(filepath, 'r') as f:
        lines = []
        for line in f.read().splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if sys.version_info[0] < 3:
                line = line.decode('utf-8')
            lines.append(line)
        return lines


def load_global_patterns():
    try:
        path = subprocess.check_output(
            ['git', 'config', '--get', 'core.excludesFile'],
            stderr=open(os.devnull, 'wb')
        ).strip()
    except OSError as e:
        if getattr(e, 'errno', None) == errno.ENOENT:
            raise GitCommandNotFound("Git is not installed or not in PATH")
        raise GlobalIgnoreLoadError("Unable to invoke git config")
    except subprocess.CalledProcessError:
        raise GitConfigMissingError("Git config does not contain core.excludesFile")

    if isinstance(path, bytes):
        path = path.decode('utf-8')
    path = os.path.expanduser(path)
    return read_patterns_from_file(path)


def load_repo_exclude_patterns(root_dir):
    exclude_path = os.path.join(root_dir, '.git', 'info', 'exclude')
    return read_patterns_from_file(exclude_path)


def load_ignore_specs(root_dir, ignore_files):
    spec_map = {}
    for dirpath, dirnames, filenames in os.walk(root_dir):
        patterns = []
        for ignore_file in ignore_files:
            ignore_path = os.path.join(dirpath, ignore_file)
            patterns.extend(read_patterns_from_file(ignore_path))

        # if this is the root dir, include repo-level patterns
        if os.path.abspath(dirpath) == os.path.abspath(root_dir):
            patterns.extend(load_repo_exclude_patterns(root_dir))
            try:
                patterns.extend(load_global_patterns())
            except GlobalIgnoreLoadError:
                pass

        if patterns:
            spec = PathSpec.from_lines(GitWildMatchPattern, patterns)
            spec_map[dirpath] = spec
    return spec_map
