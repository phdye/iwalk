# -*- coding: utf-8 -*-
import os
import sys
import tempfile
import shutil
import subprocess
import pytest


def _write_file(path, content):
    with open(path, "w") as f:
        f.write(content)


def create_tree(root):
    structure = {
        "a": {
            "file.txt": "data",
            "b": {
                "nested.txt": "deep",
                "c": {
                    "verydeep.txt": "deeper"
                }
            }
        },
        "d": {
            "sibling.txt": "sibling"
        },
        ".hidden": {
            "dotfile.txt": "hidden",
            "sub": {
                "ignored.txt": "nested hidden"
            }
        },
        "__pycache__": {
            "module.pyc": "compiled"
        },
        ".gitignore": "*.log\n*.tmp\n__pycache__/\n.ignoreme\n!.keepme.txt\n",
        "temp.tmp": "should be ignored",
        "build.log": "also ignored",
        ".ignoreme": "ignored dotfile",
        ".keepme.txt": "explicitly unignoreddeep"
    }

    def build(base, tree):
        for name, val in tree.items():
            path = os.path.join(base, name)
            if isinstance(val, dict):
                os.makedirs(path)
                build(path, val)
            else:
                _write_file(path, val)

    build(root, structure)


# Basic output test against the full tree structure with ignore rules applied
def test_iwalk_tree_output():
    temp_dir = tempfile.mkdtemp()
    try:
        create_tree(temp_dir)

        script = os.path.abspath("scripts/iwalk-tree.py")
        if not os.path.exists(script):
            pytest.skip("iwalk-tree script not found")

        proc = subprocess.Popen(
            [sys.executable, script, '--all', temp_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = proc.communicate()
        out = out.decode("utf-8")

        assert "a/" in out
        assert "b/" in out
        assert "file.txt" in out
        assert "nested.txt" in out

    finally:
        shutil.rmtree(temp_dir)


# Missing argument is fine, runs with default '.'
def test_iwalk_tree_no_args():
    script = os.path.abspath("scripts/iwalk-tree.py")
    if not os.path.exists(script):
        pytest.skip("iwalk-tree script not found")

    proc = subprocess.Popen(
        [sys.executable, script],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = proc.communicate()
    assert proc.returncode == 0  # Now allowed to run with default '.'
    assert "DEBUG" in err.decode("utf-8")

# Non-directory argument should produce error
# @pytest.mark.skipif(sys.version_info < (3, 2), reason="subprocess capture requires Python 3")
def test_iwalk_tree_with_file_arg():
    temp_dir = tempfile.mkdtemp()
    try:
        dummy_file = os.path.join(temp_dir, "dummy.txt")
        with open(dummy_file, "w") as f:
            f.write("test")

        script = os.path.abspath("scripts/iwalk-tree.py")
        if not os.path.exists(script):
            pytest.skip("iwalk-tree script not found")

        proc = subprocess.Popen(
            [sys.executable, script, dummy_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = proc.communicate()
        assert proc.returncode != 0
        assert b"Not a directory" in out or b"Not a directory" in err
    finally:
        shutil.rmtree(temp_dir)


# Hidden files should not appear if exclude_hidden=True is honored in iwalk()
# @pytest.mark.skipif(sys.version_info < (3, 2), reason="subprocess capture requires Python 3")
def test_iwalk_tree_excludes_hidden():
    temp_dir = tempfile.mkdtemp()
    try:
        create_tree(temp_dir)
        script = os.path.abspath("scripts/iwalk-tree.py")
        if not os.path.exists(script):
            pytest.skip("iwalk-tree script not found")

        proc = subprocess.Popen(
            [sys.executable, script, '--all', temp_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = proc.communicate()
        out = out.decode("utf-8")
        err = err.decode("utf-8")

        assert ".hidden/"          in out
        assert ".ignoreme"     not in out
        assert "build.log"     not in out
        assert "temp.tmp"      not in out
        assert ".keepme.txt"       in out
        assert "[DEBUG]"           in err
        assert "__pycache__/"  not in out

    finally:
        shutil.rmtree(temp_dir)
