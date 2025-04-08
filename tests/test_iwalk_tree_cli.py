# -*- coding: utf-8 -*-
import os
import sys
import tempfile
import shutil
import subprocess
import pytest


def create_tree(root):
    os.makedirs(os.path.join(root, "a", "b"))
    with open(os.path.join(root, "a", "file.txt"), "w") as f:
        f.write("data")
    with open(os.path.join(root, "a", "b", "nested.txt"), "w") as f:
        f.write("deep")


def test_iwalk_tree_output():
    temp_dir = tempfile.mkdtemp()
    try:
        create_tree(temp_dir)

        script = os.path.abspath("scripts/iwalk-tree.py")
        if not os.path.exists(script):
            pytest.skip("iwalk-tree script not found")

        proc = subprocess.Popen(
            [sys.executable, script, temp_dir],
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
