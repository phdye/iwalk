# -*- coding: utf-8 -*-
import os
import sys
import tempfile
import shutil
import pytest

from iwalk import walk


def create_file(path, content=""):
    with open(path, "w") as f:
        if sys.version_info[0] < 3:
            f.write(content.encode("utf-8"))
        else:
            f.write(content)


def test_full_walk_with_mixed_ignore():
    temp_dir = tempfile.mkdtemp()
    try:
        # Create a nested structure
        os.makedirs(os.path.join(temp_dir, "src", "__pycache__"))
        os.makedirs(os.path.join(temp_dir, ".git", "info"))
        os.makedirs(os.path.join(temp_dir, "tests"))

        create_file(os.path.join(temp_dir, ".gitignore"), "__pycache__/\n.DS_Store\ntests/ignored_test.py\n")
        create_file(os.path.join(temp_dir, ".git", "info", "exclude"), "*.bak\n")

        # Files to walk
        create_file(os.path.join(temp_dir, "README.md"))
        create_file(os.path.join(temp_dir, "src", "main.py"))
        create_file(os.path.join(temp_dir, "src", "__pycache__", "main.pyc"))
        create_file(os.path.join(temp_dir, ".DS_Store"))
        create_file(os.path.join(temp_dir, "temp.bak"))
        create_file(os.path.join(temp_dir, "tests", "test_example.py"))
        create_file(os.path.join(temp_dir, "tests", "ignored_test.py"))

        result = list(walk(temp_dir, exclude_hidden=True))

        seen = set()
        for _, _, files in result:
            for f in files:
                seen.add(f)

        assert "README.md" in seen
        assert "main.py" in seen
        assert "test_example.py" in seen

        # These should have been ignored
        assert "main.pyc" not in seen
        assert ".DS_Store" not in seen
        assert "temp.bak" not in seen
        assert "ignored_test.py" not in seen

    finally:
        shutil.rmtree(temp_dir)
