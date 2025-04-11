# Developer Guide

Welcome to the **iwalk** developer documentation. This guide is intended to help contributors and maintainers understand the project structure, compatibility goals, and best practices for working with the codebase.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Code Structure](#code-structure)
- [Compatibility Targets](#compatibility-targets)
- [Test Suite](#test-suite)
- [Debugging and Logging](#debugging-and-logging)
- [Key Design Principles](#key-design-principles)
- [Contributing Standards](#contributing-standards)

---

## Project Overview

`iwalk.walk()` is a drop-in replacement for `os.walk()` that supports `.gitignore`, `.dockerignore`, `.ignore`, and global ignore configs. It’s optimized for correctness and compatibility across Python versions from 2.7 through 3.9+.

---

## Code Structure

```plaintext
src/iwalk/
├── core.py              # walk(), is_ignored(), get_ancestor_paths()
├── patterns.py          # Pattern readers, PathSpec loaders
├── __init__.py          # Exposes public API
├── scripts/
│   └── iwalk-tree.py    # CLI demo tool
└── tests/
    ├── test_*.py        # Full test matrix with 100% coverage goal
    └── fixtures/        # Filesystem layouts for integration
```

---

## Compatibility Targets

`iwalk` is tested under:

- ✅ Python 2.7.5
- ✅ Python 3.2.5
- ✅ Python 3.9+

It avoids syntax or stdlib calls not supported in these environments, and uses `pathspec` with conditional encoding handling.

---

## Test Suite

Run tests with:

```bash
PYTHONPATH=src pytest -v
```

Each test covers:

- Hidden file exclusion
- Ignore rule precedence
- CLI integration
- Global and repo exclude behaviors

The test plan is documented in `Test-Plan.md`.

---

## Debugging and Logging

`iwalk-tree.py` uses simple `[DEBUG]` lines for visibility into:

- Root paths being walked
- Whether `exclude_hidden` was applied

You can extend this or add logging to `core.py` if needed during development.

---

## Key Design Principles

- **Minimal dependencies:** Only `pathspec` is required.
- **Pure Python:** Fully compatible with legacy runtimes.
- **Drop-in replacement:** Follows the `os.walk()` signature precisely.
- **Ignore semantics match Git:** All negation and ordering rules enforced.
- **Fails safe:** If an ignore file is unreadable, it is skipped gracefully.

---

## Contributing Standards

See [CONTRIBUTING.md](CONTRIBUTING.md) for full guidelines.

---
