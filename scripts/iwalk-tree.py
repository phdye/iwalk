#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from iwalk import iwalk

USAGE = """Usage:
  iwalk-tree.py [options] <directory>...

Options:
  -a --all       Include hidden files and directories [default: False]
  -h --help      Show this message and exit

By default, hidden files (starting with ".") are excluded from the output.
If no <directory> is given, the current working directory (.) is used.
"""

def print_tree(root, exclude_hidden):
    print("[DEBUG] Walking directory: %s (exclude_hidden=%s)" % (root, exclude_hidden))
    for dirpath, dirnames, filenames in iwalk(root, exclude_hidden=exclude_hidden):
        level = dirpath.replace(root, '').count(os.sep)
        indent = '    ' * level
        print("%s%s/" % (indent, os.path.basename(dirpath) or root))
        subindent = '    ' * (level + 1)
        for f in sorted(filenames):
            print("%s%s" % (subindent, f))

def main():
    args = sys.argv[1:]
    if '-h' in args or '--help' in args:
        print(USAGE)
        sys.exit(0)

    include_hidden = False
    cleaned_args = []

    for arg in args:
        if arg in ('-a', '--all'):
            include_hidden = True
        elif arg.startswith('-'):
            print("Unknown option: %s" % arg)
            print(USAGE)
            sys.exit(1)
        else:
            cleaned_args.append(arg)

    # Default to '.' if no directory specified
    if not cleaned_args:
        cleaned_args = ['.']

    for root in cleaned_args:
        abs_root = os.path.abspath(root)
        if not os.path.isdir(abs_root):
            print("Error: Not a directory: %s" % root)
            sys.exit(1)
        print_tree(abs_root, exclude_hidden=not include_hidden)

if __name__ == "__main__":
    main()
