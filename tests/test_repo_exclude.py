# -*- coding: utf-8 -*-
import os
import sys
import tempfile
import shutil
import pytest

from iwalk.patterns import read_patterns_from_file, load_repo_exclude_patterns


def make_repo_exclude_file(contents):
    temp_dir = tempfile.mkdtemp()
    git_info_dir = os.path.join(temp_dir, ".git", "info")
    os.makedirs(git_info_dir)
    exclude_path = os.path.join(git_info_dir, "exclude")
    with open(exclude_path, "w") as f:
        if sys.version_info[0] < 3:
            f.write(contents.encode("utf-8"))
        else:
            f.write(contents)
    return exclude_path, temp_dir


# ✅ Test: Loads patterns from a standard .git/info/exclude file
def test_load_info_exclude():
    exclude_path, temp_dir = make_repo_exclude_file("*.bak\n!important.bak\n")
    try:
        patterns = load_repo_exclude_patterns(temp_dir)
        assert patterns == ["*.bak", "!important.bak"]
    finally:
        shutil.rmtree(temp_dir)


# ✅ Test: Gracefully returns empty list if .git/info/exclude file does not exist
def test_missing_exclude_file():
    temp_dir = tempfile.mkdtemp()
    try:
        patterns = load_repo_exclude_patterns(temp_dir)
        assert patterns == []
    finally:
        shutil.rmtree(temp_dir)
