---

###  Python File and Directory Functions That Could Benefit

| ihonor               | Function or Module                      | Enhancement with Ignore Support |
|----------------------------------------|----------------------------------|----------------------------------|
| ilistdir()          | `os.listdir()`                         | Filter out ignored/hidden files in a single directory |
| iscandir()               | `os.scandir()`                         | Provide an iterator over visible/non-ignored entries |
| iglob() | `glob.glob()` / `pathlib.Path.glob()`  | Exclude results based on ignore rules, especially recursive `**/*.py` patterns |
| icopytree()         | `shutil.copytree()`                    | Skip ignored files while copying directories |
|               | `shutil.rmtree()`                      | Avoid deleting ignored files or directories unintentionally |
| *perhaps* | `zipfile.ZipFile.write()`              | Automatically exclude ignored files from archives |
| *perhaps* | `tarfile.add()`                        | Filter archived contents via ignore rules |
|               | `os.path.walk()` (legacy)              | Can be retrofitted similar to `os.walk()` |
|  | Custom CLI tools (e.g., linters, indexers, formatters) | All filesystem scans could leverage `iwalk` or an ignore-enhanced wrapper to skip unwanted files |

---

### 💡 iwalk-Compatible Alternatives

Some higher-level utilities or CLI tools may define their own internal walkers or directory processors. For these cases:

- Refactor internal traversal to **wrap `iwalk.walk()`** instead of `os.walk()`.
- Inject a custom `filter_entries()` method that honors ignore rules.

---

### 🧪 Suggested Additions to iwalk (Future Enhancements)

Based on the design in `Design.md`, the following might be clean extensions:

- `iwalk.listdir(path, exclude_hidden=False)`
- `iwalk.scandir(path, exclude_hidden=False)`
- `iwalk.copytree(src, dst, ignore_rules=True)`
- `iwalk.glob(pattern, ignore_rules=True)`
- `iwalk.archive(root_dir, format='zip', ignore_rules=True)`

These would serve as drop-in filtered versions of the standard functions, aligned with Git-style ignore behavior.

Would you like a draft implementation of any of these enhancements?