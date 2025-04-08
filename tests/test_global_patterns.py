# -*- coding: utf-8 -*-
import os
import sys
import tempfile
import shutil
import subprocess
import pytest

from iwalk.patterns import load_global_patterns, GitCommandNotFound, GitConfigMissingError


# Utility: Creates a temporary ignore file with the given contents
def make_temp_ignore_file(contents):
    temp_dir = tempfile.mkdtemp()
    ignore_file = os.path.join(temp_dir, "global_ignore")
    with open(ignore_file, "w") as f:
        if sys.version_info[0] < 3:
            f.write(contents.encode("utf-8"))
        else:
            f.write(contents)
    return ignore_file, temp_dir


# ✅ Test: Verifies that GitCommandNotFound is raised when git is missing
# Purpose: Ensure git-not-found leads to specific exception
# Expected: GitCommandNotFound is raised

def test_fails_when_git_not_found(monkeypatch):
    def fake_check_output(*args, **kwargs):
        import errno
        raise OSError(errno.ENOENT, "No such file or directory")
    monkeypatch.setattr(subprocess, "check_output", fake_check_output)
    with pytest.raises(GitCommandNotFound):
        load_global_patterns()


# ✅ Test: Verifies that GitConfigMissingError is raised when config is unset
# Purpose: Ensure missing config triggers a specific error
# Expected: GitConfigMissingError is raised

def test_fails_when_git_config_missing(monkeypatch):
    def fake_check_output(*args, **kwargs):
        raise subprocess.CalledProcessError(1, args[0])
    monkeypatch.setattr(subprocess, "check_output", fake_check_output)
    with pytest.raises(GitConfigMissingError):
        load_global_patterns()


# ✅ Test: Loads patterns from a file path returned by mocked git config
# Purpose: Simulate 'git config core.excludesFile' and check pattern parsing
# Expected: The parsed patterns should match the test content

def test_loads_from_git_config(monkeypatch):
    ignore_file, temp_dir = make_temp_ignore_file("*.log\n!important.log\n")
    assert os.path.exists(ignore_file), "Ignore file not found at path used in monkeypatch"
    try:
        ignore_line = (ignore_file + "\n").encode("utf-8") if sys.version_info[0] >= 3 else (ignore_file + "\n")
        monkeypatch.setattr(
            subprocess, "check_output",
            lambda *args, **kwargs: ignore_line
        )
        patterns = load_global_patterns()
        assert patterns == ["*.log", "!important.log"]
    finally:
        shutil.rmtree(temp_dir)


# ✅ Test: Tests comment-only file returned by simulated git config
# Purpose: Ensure comment lines and blank lines are ignored
# Expected: Empty list of patterns

def test_returns_empty_for_empty_file(monkeypatch):
    ignore_file, temp_dir = make_temp_ignore_file("\n# comment only\n\n")
    monkeypatch.setattr(
        subprocess, "check_output",
        lambda *args, **kwargs: ignore_file.encode("utf-8") if sys.version_info[0] >= 3 else ignore_file
    )
    try:
        patterns = load_global_patterns()
        assert patterns == []
    finally:
        shutil.rmtree(temp_dir)
