## ✅ iwalk Test Suite Overview

### 📂 Test Suite Structure (Filesystem)
```plaintext
tests/
├── __init__.py
├── test_read_patterns.py
├── test_global_patterns.py
├── test_repo_exclude.py
├── test_ignore_specs.py
├── test_ignore_checker.py
├── test_walk.py
├── test_hidden_exclude.py
├── test_backwards_compatibility.py
└── fixtures/
    └── complex_structure/
```

Each test module covers a distinct aspect of the design document with 100% coverage goal.

---

## 🔬 Test Modules and Coverage

### `test_read_patterns.py`

#### ✅ Test Matrix

| Test Case | Description |
|----------|-------------|
| `test_blank_lines_removed` | Patterns file with empty lines |
| `test_comment_lines_ignored` | Ignores lines starting with `#` |
| `test_unicode_and_whitespace` | Handles UTF-8 and trailing whitespace |
| `test_missing_file_returns_empty` | Returns empty list if file doesn’t exist |
| `test_windows_line_endings` | Handles CRLF line endings correctly |

---

### `test_global_patterns.py`

| Test Case | Description |
|----------|-------------|
| `test_load_from_default_home_config` | Loads from `~/.gitignore_global` |
| `test_load_custom_global_path` | Custom global ignore path via env var |
| `test_invalid_global_path_returns_empty` | Handles missing/invalid path gracefully |

---

### `test_repo_exclude.py`

| Test Case | Description |
|----------|-------------|
| `test_load_info_exclude` | Loads from `.git/info/exclude` |
| `test_missing_exclude_file` | Gracefully skips if file missing |
| `test_combination_with_local_gitignore` | Merges local `.gitignore` and `.git/info/exclude` |

---

### `test_ignore_specs.py`

| Test Case | Description |
|----------|-------------|
| `test_single_dir_gitignore` | `.gitignore` in one subdir only |
| `test_ignore_overrides_with_negation` | Test negation `!important.txt` |
| `test_combined_global_repo_dir_patterns` | Test proper merging of all levels |
| `test_pathspec_correct_patterns_loaded` | Verifies `PathSpec` receives correct patterns |

---

### `test_ignore_checker.py`

| Test Case | Description |
|----------|-------------|
| `test_basic_ignores` | Basic pattern exclusion |
| `test_nested_ancestor_patterns` | Ignores from parent dirs |
| `test_negation_wins_later` | `!` pattern restores visibility |
| `test_hidden_files_ignored_when_flag_false` | Respects `exclude_hidden` flag |
| `test_path_relative_handling` | Paths interpreted correctly from root dir |

---

### `test_walk.py`

| Test Case | Description |
|----------|-------------|
| `test_basic_walk_no_ignores` | Should match `os.walk()` output exactly |
| `test_walk_with_ignores` | Excludes files per `.gitignore` |
| `test_walk_with_hidden_excluded` | Excludes `.*` if flag enabled |
| `test_symlinks_behavior` | Tests symlink traversal (if supported) |
| `test_directory_with_many_ignores` | Deeply nested `.gitignore` handling |
| `test_file_and_dir_same_name` | Handles conflicting ignore rules for dir/file named `log` |

---

### `test_hidden_exclude.py`

| Test Case | Description |
|----------|-------------|
| `test_exclude_hidden_files_flag` | Excludes files starting with `.` |
| `test_exclude_hidden_dirs_flag` | Excludes dirs starting with `.` |
| `test_combined_hidden_and_ignored` | Hidden + `.gitignore` combined |

---

### `test_backwards_compatibility.py`

Follows guidance from `Supporting-Backports.md`

| Test Case | Description |
|----------|-------------|
| `test_python27_compatibility_walk` | Uses Python 2.7 interpreter via Tox |
| `test_all_features_polyfill` | Validates `six` or compatibility layer |
| `test_read_patterns_backport` | Ensures pattern loading behaves the same |
| `test_print_unicode_and_paths_py2` | Handles encoding, path differences cleanly |
| `test_absolute_and_relative_paths_py2_py3` | Ensures output consistency across versions |

---

## 🧪 Integration and Edge Case Scenarios

### Fixture: `tests/fixtures/complex_structure/`
A comprehensive directory tree that includes:

- `.gitignore` with `*`, `!keepme.txt`
- `dir/.gitignore` with recursive ignores
- `dir/.hidden/`
- `dir/deep/.git/info/exclude`
- Symlink loops (if allowed)
- Files with `#commented` names
- Unicode file names (`тест.txt`)
- Files with trailing whitespace, tab characters

Used in `test_walk.py` and other modules.

---

## ⚙️ Automation and CI

### Tox Config
```ini
[tox]
envlist = py27, py38

[testenv]
deps =
    pytest
    pathspec
    six
commands = pytest
```

### GitHub Actions (example)
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [2.7, 3.8]
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - run: pip install tox
      - run: tox
```

---

## 📖 Extras

### Coverage Goal: 100%

Use `pytest --cov=iwalk` to generate line and branch coverage stats.

---

