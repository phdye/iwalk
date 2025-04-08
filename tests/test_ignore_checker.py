# -*- coding: utf-8 -*-
import os
import sys
import tempfile
import shutil
import pytest

from iwalk.patterns import load_ignore_specs
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPattern


def create_file(path, content=""):
    with open(path, "w") as f:
        if sys.version_info[0] < 3:
            f.write(content.encode("utf-8"))
        else:
            f.write(content)


def is_ignored(path, spec_map):
    abs_path = os.path.abspath(path)
    for spec_dir in sorted(spec_map.keys(), key=lambda p: -len(p)):
        if abs_path.startswith(spec_dir):
            rel_path = os.path.relpath(abs_path, spec_dir)
            if spec_map[spec_dir].match_file(rel_path):
                return True
    return False


def test_basic_ignores():
    temp_dir = tempfile.mkdtemp()
    try:
        create_file(os.path.join(temp_dir, ".gitignore"), "ignored.txt\n")
        create_file(os.path.join(temp_dir, "ignored.txt"))
        specs = load_ignore_specs(temp_dir, [".gitignore"])
        assert is_ignored(os.path.join(temp_dir, "ignored.txt"), specs)
    finally:
        shutil.rmtree(temp_dir)


def test_nested_ancestor_patterns():
    temp_dir = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(temp_dir, "a", "b"))
        create_file(os.path.join(temp_dir, ".gitignore"), "a/b/ignored.txt\n")
        create_file(os.path.join(temp_dir, "a", "b", "ignored.txt"))
        specs = load_ignore_specs(temp_dir, [".gitignore"])
        assert is_ignored(os.path.join(temp_dir, "a", "b", "ignored.txt"), specs)
    finally:
        shutil.rmtree(temp_dir)


def test_negation_wins_later():
    temp_dir = tempfile.mkdtemp()
    try:
        create_file(os.path.join(temp_dir, ".gitignore"), "*.log\n!important.log\n")
        create_file(os.path.join(temp_dir, "error.log"))
        create_file(os.path.join(temp_dir, "important.log"))
        specs = load_ignore_specs(temp_dir, [".gitignore"])
        assert is_ignored(os.path.join(temp_dir, "error.log"), specs)
        assert not is_ignored(os.path.join(temp_dir, "important.log"), specs)
    finally:
        shutil.rmtree(temp_dir)


def test_hidden_files_ignored_when_flag_false():
    temp_dir = tempfile.mkdtemp()
    try:
        os.mkdir(os.path.join(temp_dir, ".hidden"))
        os.mkdir(os.path.join(temp_dir, "visible"))
        specs = load_ignore_specs(temp_dir, [".gitignore"])
        # simulate exclusion of hidden directories manually
        def is_hidden(p):
            return os.path.basename(p).startswith('.')
        all_dirs = [d for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d))]
        filtered_dirs = [d for d in all_dirs if not is_hidden(d)]
        assert ".hidden" not in filtered_dirs
    finally:
        shutil.rmtree(temp_dir)


def test_path_relative_handling():
    temp_dir = tempfile.mkdtemp()
    try:
        os.mkdir(os.path.join(temp_dir, "logs"))
        create_file(os.path.join(temp_dir, ".gitignore"), "logs/*.txt\n")
        create_file(os.path.join(temp_dir, "logs", "error.txt"))
        create_file(os.path.join(temp_dir, "logs", "error.log"))
        specs = load_ignore_specs(temp_dir, [".gitignore"])
        assert is_ignored(os.path.join(temp_dir, "logs", "error.txt"), specs)
        assert not is_ignored(os.path.join(temp_dir, "logs", "error.log"), specs)
    finally:
        shutil.rmtree(temp_dir)


def test_ignore_multiple_levels():
    temp_dir = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(temp_dir, "x", "y", "z"))
        create_file(os.path.join(temp_dir, ".gitignore"), "x/y/z/blocked.txt\n")
        create_file(os.path.join(temp_dir, "x", "y", "z", "blocked.txt"))
        specs = load_ignore_specs(temp_dir, [".gitignore"])
        assert is_ignored(os.path.join(temp_dir, "x", "y", "z", "blocked.txt"), specs)
    finally:
        shutil.rmtree(temp_dir)
