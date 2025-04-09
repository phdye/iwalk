# Contributing to iwalk

Thank you for considering a contribution to the **iwalk** project!

This document describes how to report issues, propose changes, and write patches that conform to the project’s expectations.

---

## Table of Contents

- [Reporting Issues](#reporting-issues)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing Requirements](#testing-requirements)
- [Commit Messages](#commit-messages)
- [Backport Support](#backport-support)
- [Pull Request Guidelines](#pull-request-guidelines)

---

## Reporting Issues

Please report bugs, incorrect ignore behavior, or compatibility issues via GitHub issues. Include:

- OS and Python version
- `iwalk` version (if tagged)
- Test case or `.gitignore`/file tree setup

---

## Development Workflow

1. Clone the repo and install dev dependencies (pytest, pathspec).
2. Make edits in `src/iwalk/`.
3. Add or update tests in `tests/`.
4. Confirm full test suite passes:

```bash
PYTHONPATH=src pytest -v
```

5. Submit a PR with a clear description.

---

## Code Style

- Keep Python 2.7 compatibility in mind.
- Use no f-strings or type annotations unless inside comments.
- Follow PEP8 (use 4 spaces, max 100 cols).

---

## Testing Requirements

All code must include corresponding tests.

Run:

```bash
tox
```

To validate against both Python 2.7 and Python 3.8+ (see `.tox.ini`).

---

## Commit Messages

Use imperative, present tense. Example:

```
Fix handling of nested .gitignore negation
```

---

## Backport Support

- Avoid `pathlib`, `typing`, and `f-strings`
- Prefer `os.path`, `fnmatch`, and `re`
- Conditional logic for `sys.version_info` is acceptable for encoding and IO

---

## Pull Request Guidelines

- Include test coverage for your change.
- Don’t break compatibility or remove behavior silently.
- Be respectful and constructive in discussion.

---

Thank you again for contributing to iwalk!
