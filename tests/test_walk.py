import os
import sys
import tempfile
import shutil

# Import the correct walk version based on sys.version_info
from iwalk import iwalk

def create_file(path, content=""):
    with open(path, "w") as f:
        f.write(content)

def test_walk_basic_ignore():
    temp_dir = tempfile.mkdtemp()
    try:
        os.mkdir(os.path.join(temp_dir, "subdir"))
        create_file(os.path.join(temp_dir, "file1.txt"))
        create_file(os.path.join(temp_dir, ".gitignore"), "file1.txt\n")

        result = list(iwalk(temp_dir))
        assert len(result) == 2
        for dirpath, dirnames, filenames in result:
            assert "file1.txt" not in filenames
    finally:
        shutil.rmtree(temp_dir)

def test_walk_exclude_hidden():
    temp_dir = tempfile.mkdtemp()
    try:
        os.mkdir(os.path.join(temp_dir, ".hidden"))
        os.mkdir(os.path.join(temp_dir, "visible"))
        create_file(os.path.join(temp_dir, "visible", "file.txt"))
        create_file(os.path.join(temp_dir, ".hidden", "file.txt"))

        result = list(iwalk(temp_dir, exclude_hidden=True))
        for dirpath, dirnames, filenames in result:
            assert ".hidden" not in dirnames
            assert "file.txt" not in filenames or not dirpath.endswith(".hidden")
    finally:
        shutil.rmtree(temp_dir)

def test_walk_with_nested_gitignore():
    temp_dir = tempfile.mkdtemp()
    try:
        os.makedirs(os.path.join(temp_dir, "a", "b"))
        create_file(os.path.join(temp_dir, "a", "b", "secret.txt"))
        create_file(os.path.join(temp_dir, "a", ".gitignore"), "b/\n")

        result = list(iwalk(temp_dir))
        for dirpath, dirnames, filenames in result:
            assert not any("secret.txt" in f for f in filenames)
    finally:
        shutil.rmtree(temp_dir)
