import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'vendor')))
from pathspec import PathSpec
from pathspec.patterns.gitwildmatch import GitWildMatchPattern

IGNORE_FILENAMES = ['.gitignore', '.dockerignore', '.ignore']

def walk(
    root_dir: str,
    ignore_files = IGNORE_FILENAMES,
    exclude_hidden = False
) :
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

def load_ignore_specs(root_dir: str, ignore_files: str) :
    """
    Loads all supported ignore files and maps PathSpecs to directories.
    """
    spec_map = {}
    global_patterns = load_global_patterns()
    repo_exclude_patterns = load_repo_exclude_patterns(root_dir)

    for dirpath, _, filenames in os.walk(root_dir):
        patterns = []
        for ignore_name in ignore_files:
            ignore_path = os.path.join(dirpath, ignore_name)
            patterns.extend(read_patterns_from_file(ignore_path))
        if dirpath == root_dir:
            patterns.extend(repo_exclude_patterns)
        if patterns:
            spec_map[os.path.abspath(dirpath)] = PathSpec.from_lines(GitWildMatchPattern, patterns)

    # Add global patterns to root directory spec
    if global_patterns:
        root_abs = os.path.abspath(root_dir)
        if root_abs not in spec_map:
            spec_map[root_abs] = PathSpec.from_lines(GitWildMatchPattern, global_patterns)
        else:
            combined = spec_map[root_abs].patterns + PathSpec.from_lines(GitWildMatchPattern, global_patterns).patterns
            spec_map[root_abs] = PathSpec(combined)

    return spec_map

def is_ignored(path, spec_map):
    abs_path = os.path.abspath(path)
    for ancestor in [abs_path] + get_ancestor_paths(abs_path):
        if ancestor in spec_map:
            rel_path = os.path.relpath(abs_path, ancestor)
            if spec_map[ancestor].match_file(rel_path):
                return True
    return False

def get_ancestor_paths(path: str) :
    paths = []
    parent = os.path.dirname(path)
    while parent and parent != path:
        paths.append(parent)
        path, parent = parent, os.path.dirname(parent)
    return paths

def load_repo_exclude_patterns(root_dir: str) :
    exclude_path = os.path.join(root_dir, '.git', 'info', 'exclude')
    return read_patterns_from_file(exclude_path)

def load_global_patterns() :
    paths = [
        os.path.expanduser('~/.gitignore_global'),
        os.path.expanduser('~/.config/git/ignore')
    ]
    patterns = []
    for path in paths:
        patterns.extend(read_patterns_from_file(path))
    return patterns

def read_patterns_from_file(filepath: str) :
    if not os.path.isfile(filepath):
        return []
    with open(filepath, 'r') as f:
        return [
            line.strip() for line in f.read().splitlines()
            if line.strip() and not line.strip().startswith('#')
        ]
