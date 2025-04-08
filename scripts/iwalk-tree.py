#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from iwalk import walk

def print_tree(root):
    for dirpath, dirnames, filenames in walk(root):
        level = dirpath.replace(root, '').count(os.sep)
        indent = '    ' * level
        print("%s%s/" % (indent, os.path.basename(dirpath) or root))
        subindent = '    ' * (level + 1)
        for f in sorted(filenames):
            print("%s%s" % (subindent, f))

def main():
    if len(sys.argv) < 2:
        print("Usage: ptree <directory>")
        sys.exit(1)
    root = os.path.abspath(sys.argv[1])
    if not os.path.isdir(root):
        print("Error: Not a directory: %s" % root)
        sys.exit(1)
    print_tree(root)


if __name__ == "__main__":
    main()
