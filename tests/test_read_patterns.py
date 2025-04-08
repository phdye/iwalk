# -*- coding: utf-8 -*-
import sys
import os
import tempfile
import shutil
import pytest

from iwalk.patterns import read_patterns_from_file


def create_temp_ignore_file(contents):
    temp_dir = tempfile.mkdtemp()
    ignore_path = os.path.join(temp_dir, ".gitignore")
    with open(ignore_path, "w") as f:
        if sys.version_info[0] < 3:
            f.write(contents.encode("utf-8"))
        else:
            f.write(contents)
    return ignore_path, temp_dir


def remove_temp_dir(temp_dir):
    shutil.rmtree(temp_dir)


def test_blank_lines_removed():
    ignore_file, temp_dir = create_temp_ignore_file("""


    # comment
    foo.txt


    """)
    try:
        patterns = read_patterns_from_file(ignore_file)
        assert patterns == ["foo.txt"]
    finally:
        remove_temp_dir(temp_dir)


def test_comment_lines_ignored():
    ignore_file, temp_dir = create_temp_ignore_file("""
    # this is a comment
    bar.log
    # another comment
    """)
    try:
        patterns = read_patterns_from_file(ignore_file)
        assert patterns == ["bar.log"]
    finally:
        remove_temp_dir(temp_dir)

def test_unicode_and_whitespace():
    contents = b"  spaced.txt  \n  \\u0442\\u0435\\u0441\\u0442.txt\n".decode("unicode_escape")
    ignore_file, temp_dir = create_temp_ignore_file(contents)
    try:
        patterns = read_patterns_from_file(ignore_file)
        expected_unicode = b"\u0442\u0435\u0441\u0442.txt".decode("unicode_escape")
        assert patterns == ["spaced.txt", expected_unicode]
    finally:
        remove_temp_dir(temp_dir)

def test_missing_file_returns_empty():
    missing_path = "/nonexistent/.gitignore"
    patterns = read_patterns_from_file(missing_path)
    assert patterns == []


def test_windows_line_endings():
    ignore_file, temp_dir = create_temp_ignore_file("line1\r\nline2\r\n")
    try:
        patterns = read_patterns_from_file(ignore_file)
        assert patterns == ["line1", "line2"]
    finally:
        remove_temp_dir(temp_dir)
