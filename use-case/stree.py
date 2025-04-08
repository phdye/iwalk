#!/usr/bin/env python3

"""
stree - Selective Tree
A simple Python script to generate a filtered directory tree display.

Usage:
  stree [options] [<path>...]
  stree (-h | --help)
  stree --version

Arguments:
  <path>...    One or more files or directories to include in the filtered tree.

  <path>'s can be absolute or relative.

  <path>:
    None         No path provided, defaults to current directory.
    Directory    Include all contents of the directory.
    File         Include the containing directory of the file.
    Symlink      Include the target of the symlink.

Options:
  -d, --dirs       Show only directories in the output (skip files).
  -f, --full       Display full paths instead of base names.
  -s, --sort       Sort by full path alphabetically (default: insertion order).
  -b, --bsort      Sort by basename instead of full path.
  -r, --reverse    Reverse sort order.
  -h, --help       Show this help message and exit.
  -v, --version    Show version and exit.

Description:
  stree (Selective Tree) generates a filtered directory tree display for a
  given set of files and/or folders, relative to the current working directory.

  Unlike the standard 'tree' command, `stree` limits its display strictly to
  the provided inputs, their ancestors and children, making it ideal for
  visualizing project subsets, changed files, or configs.

Examples:

  stree src/ docs/
      Show only paths under src/ and docs/ as a tree.

  stree -d .git .github
      Show only directory structure under .git and .github folders.

  stree -f -s my_file.py setup.py
      Show full sorted paths for listed files and their containing folders.

  stree --version
      Show version information.
"""

import os
import sys
from collections import defaultdict

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "vendor")))
from docopt import docopt

# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from iwalk import walk as iwalk # complies with .gitignore, .dockerignore, etc.

__version__ = "1.1.0"


def build_filtered_paths(root, filters, dirs_only):
    filtered = set()
    for item in filters:
        full = os.path.abspath(os.path.join(root, item))
        if os.path.isfile(full):
            if not dirs_only:
                rel = os.path.relpath(full, root)
                filtered.add(rel)
            filtered.add(".")
        elif os.path.isdir(full):
            for dirpath, dirnames, filenames in iwalk(full):
                rel_dir = os.path.relpath(dirpath, root)
                filtered.add(rel_dir if rel_dir != "." else ".")
                if not dirs_only:
                    for f in filenames:
                        filtered.add(os.path.join(rel_dir, f))
    return filtered


def build_tree(paths, sort=False, reverse=False, basesort=False):
    tree = defaultdict(list)
    if sort:
        items = sorted(paths, key=(os.path.basename if basesort else None))
    else:
        items = list(paths)
    if reverse:
        items = list(reversed(items))
    for path in items:
        if path == ".":
            continue
        parent = os.path.dirname(path) or "."
        tree[parent].append(path)
    return tree


def print_tree(node, tree, prefix="", full_path=False):
    children = tree.get(node, [])
    for idx, child in enumerate(children):
        is_last = idx == len(children) - 1
        connector = "└── " if is_last else "├── "
        name = os.path.abspath(child) if full_path else os.path.basename(child)
        print(prefix + connector + name)
        if child in tree:
            extension = "    " if is_last else "│   "
            print_tree(child, tree, prefix + extension, full_path)


def main():
    args = docopt(__doc__, version=__version__)

    filters = args["<path>"] or ["."]
    root = os.getcwd()
    dirs_only = args["--dirs"]
    full_path = args["--full"]
    sort = args["--sort"]
    basesort = args["--bsort"]
    reverse = args["--reverse"]

    paths = build_filtered_paths(root, filters, dirs_only)
    if not paths:
        paths.add(".")
    tree = build_tree(paths, sort, reverse, basesort)
    print(".")
    print_tree(".", tree, full_path=full_path)
    return 0


if __name__ == "__main__":
    exit(main())
