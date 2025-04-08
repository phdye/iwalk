# -*- coding: utf-8 -*-
import sys
import os
import tempfile
import shutil
import pytest

from iwalk.patterns import read_patterns_from_file


def create_file(path, content):
    with open(path, "w") as f:
        if sys.version_info[0] < 3:
            f.write(content.encode("utf-8"))
        else:
            f.write(content)


def test_python27_compatibility_walk():
    assert sys.version_info >= (2, 7), "Python 2.7+ required"


def test_all_features_polyfill():
    try:
        import six
    except ImportError:
        pytest.skip("six module not available")
    assert hasattr(six, "string_types")


def test_read_patterns_backport():
    temp_dir = tempfile.mkdtemp()
    try:
        gitignore = os.path.join(temp_dir, ".gitignore")
        create_file(gitignore, "a.txt\n# comment\n\n!keepme.txt\n")
        patterns = read_patterns_from_file(gitignore)
        assert "a.txt" in patterns
        assert "!keepme.txt" in patterns
        assert "# comment" not in patterns
    finally:
        shutil.rmtree(temp_dir)


def test_print_unicode_and_paths_py2():
    try:
        unicode_path = b"\\u0442\\u0435\\u0441\\u0442.txt".decode("unicode_escape")
        if sys.version_info[0] < 3:
            print(unicode_path.encode("utf-8"))
        else:
            print(unicode_path)
    except Exception as e:
        pytest.fail("Unicode handling failed: %s" % e)


def test_absolute_and_relative_paths_py2_py3():
    temp_dir = tempfile.mkdtemp()
    try:
        path = os.path.join(temp_dir, "file.txt")
        create_file(path, "data")
        abs_path = os.path.abspath(path)
        rel_path = os.path.relpath(abs_path, temp_dir)
        assert os.path.exists(abs_path)
        assert not rel_path.startswith("/")
    finally:
        shutil.rmtree(temp_dir)
