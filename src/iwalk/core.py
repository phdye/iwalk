import os
from iwalk.patterns import load_ignore_specs

IGNORE_FILENAMES = ['.gitignore', '.dockerignore', '.ignore']

def iwalk(root_dir, ignore_files=IGNORE_FILENAMES, exclude_hidden=False):
    root_dir = os.path.abspath(root_dir)
    spec_map = load_ignore_specs(root_dir, ignore_files)

    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        dirnames[:] = [
            d for d in dirnames
            if not is_ignored(os.path.join(dirpath, d), spec_map)
            and (not exclude_hidden or not d.startswith('.'))
        ]
        filtered_files = [
            f for f in filenames
            if not is_ignored(os.path.join(dirpath, f), spec_map)
            and (not exclude_hidden or not f.startswith('.'))
        ]
        yield dirpath, dirnames, filtered_files

def is_ignored(path, spec_map):
    abs_path = os.path.abspath(path)
    is_dir = os.path.isdir(abs_path)
    for ancestor in [abs_path] + get_ancestor_paths(abs_path):
        if ancestor in spec_map:
            rel_path = os.path.relpath(abs_path, ancestor)
            # Try matching without a trailing slash.
            if spec_map[ancestor].match_file(rel_path):
                return True
            # For directories, also try matching with a trailing slash.
            if is_dir and spec_map[ancestor].match_file(rel_path + os.sep):
                return True
    return False

def get_ancestor_paths(path):
    paths = []
    parent = os.path.dirname(path)
    while parent and parent != path:
        paths.append(parent)
        path, parent = parent, os.path.dirname(parent)
    return paths
