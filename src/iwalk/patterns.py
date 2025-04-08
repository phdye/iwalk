# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import errno

from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPattern

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
    # print("\nreading: %r" % filepath)
    # print("isfile:", os.path.isfile(filepath))
    # sys.stdout.flush()
    if not os.path.isfile(filepath):
        return []
    with open(filepath, 'r') as f:
        lines = []
        for line in f.read().splitlines():
            line = line.strip()
            if not line or line.strip().startswith('#'):
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
    # print("\n\ngit config path [1]:" + path + "\n")
    path = os.path.expanduser(path)
    # print("\n\ngit config path [2]:" + path + "\n")
    # sys.stdout.flush()
    return read_patterns_from_file(path)


def load_repo_exclude_patterns(root_dir):
    exclude_path = os.path.join(root_dir, '.git', 'info', 'exclude')
    return read_patterns_from_file(exclude_path)
