# iwalk

**iwalk** is a Python drop-in replacement for `os.walk()` that respects `.gitignore`, `.dockerignore`, `.ignore`, and global ignore configurations. It behaves like Git when deciding which files and directories to ignore, making it ideal for backup tools, file processors, and development utilities.

[![PyPI version](https://badge.fury.io/py/iwalk.svg)](https://pypi.org/project/iwalk/)
[![CI](https://github.com/yourname/iwalk/actions/workflows/test.yml/badge.svg)](https://github.com/yourname/iwalk/actions)

---

## 🚀 Features

- 🧠 Honors `.gitignore`, `.dockerignore`, `.ignore`, and user-level ignore rules
- 🧱 Compatible with **Python 2.7**, **3.2**, and modern 3.x versions
- 🔁 Drop-in compatible with `os.walk()`
- ⚙️ Toggle hidden files, follow symlinks, or customize ignore sources
- 🧪 Tested on real `.gitignore` trees

---

## 📦 Installation

```bash
pip install iwalk
```

---

## 🧑‍💻 Usage

```python
from iwalk import walk

for dirpath, dirnames, filenames in walk("my_project", exclude_hidden=True):
    print(dirpath, filenames)
```

To ignore hidden files and respect all ignore rules, you're done. No configuration needed.

---

## 📄 CLI Tool

```bash
python -m iwalk.scripts.iwalk-tree <directory> [--all]
```

- `--all`: Show hidden files too
- Defaults to `.` if no directory is provided

---

## 🧪 Testing

```bash
pytest -v
```

All test cases are in `tests/`. Coverage includes ignore rules, CLI behavior, global patterns, and mixed setups.

---

## 🔄 Compatibility

Python versions supported:

- ✅ Python 2.7
- ✅ Python 3.2
- ✅ Python 3.6–3.12+

Platform support:

- Linux, macOS, Windows (including Cygwin)

---

## 🤝 Contributing

Pull requests are welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) and [Developer Guide](doc/Developer-Guide.md) before submitting a PR.

---

## 📚 Documentation

- [Developer Guide](doc/Developer-Guide.md)
- [Contribution Guidelines](CONTRIBUTING.md)

---

## 📄 License

MIT License © 2025 [Your Name or Org]

---
