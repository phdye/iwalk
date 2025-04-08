# -*- coding: utf-8 -*-
import os
import sys
import tempfile
import shutil
import pytest
import subprocess

from iwalk.patterns import load_ignore_specs


def create_file(path, content=""):
    with open(path, "w") as f:
        if sys.version_info[0] < 3:
            f.write(content.encode("utf-8"))
        else:
            f.write(content)


def test_single_dir_gitignore():
    temp_dir = tempfile.mkdtemp()
    try:
        os.mkdir(os.path.join(temp_dir, "subdir"))
        create_file(os.path.join(temp_dir, ".gitignore"), "ignored.txt\n")
        specs = load_ignore_specs(temp_dir, [".gitignore"])
        assert os.path.join(temp_dir) in specs
        assert specs[os.path.join(temp_dir)].match_file("ignored.txt")
    finally:
        shutil.rmtree(temp_dir)


def test_ignore_overrides_with_negation():
    temp_dir = tempfile.mkdtemp()
    try:
        create_file(os.path.join(temp_dir, ".gitignore"), "*.log\n!important.log\n")
        specs = load_ignore_specs(temp_dir, [".gitignore"])
        spec = specs[temp_dir]
        assert spec.match_file("error.log")
        assert not spec.match_file("important.log")
    finally:
        shutil.rmtree(temp_dir)


def test_combined_global_repo_dir_patterns(monkeypatch):
    temp_dir = tempfile.mkdtemp()
    try:
        os.mkdir(os.path.join(temp_dir, ".git"))
        os.makedirs(os.path.join(temp_dir, ".git", "info"))
        create_file(os.path.join(temp_dir, ".gitignore"), "local.txt\n")
        create_file(os.path.join(temp_dir, ".git", "info", "exclude"), "excluded.txt\n")

        def fake_check_output(*args, **kwargs):
            raise subprocess.CalledProcessError(1, args[0])  # prevent global pattern injection

        monkeypatch.setattr(subprocess, "check_output", fake_check_output)

        specs = load_ignore_specs(temp_dir, [".gitignore"])
        root_spec = specs[temp_dir]
        assert root_spec.match_file("local.txt")
        assert root_spec.match_file("excluded.txt")
    finally:
        shutil.rmtree(temp_dir)


def test_pathspec_correct_patterns_loaded():
    temp_dir = tempfile.mkdtemp()
    try:
        create_file(os.path.join(temp_dir, ".gitignore"), "*.tmp\n")
        specs = load_ignore_specs(temp_dir, [".gitignore"])
        spec = specs[temp_dir]
        assert spec.match_file("file.tmp")
        assert not spec.match_file("file.txt")
    finally:
        shutil.rmtree(temp_dir)
