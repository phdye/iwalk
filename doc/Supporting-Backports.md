Supporting modern Python packages that also run on legacy versions like Python 2.7.5 is challenging but achievable with a thoughtful strategy. The key is to organize your project in a way that minimizes divergence between versions while ensuring that you are using tools and patterns known to work across the supported versions. Here are the best practices to help you manage backports effectively:

---

### 1. Maintain a Clean Codebase with Compatibility Layers

- **Use a Compatibility Library:**  
  Libraries such as [six](https://pypi.org/project/six/) or [future](https://pypi.org/project/future/) can bridge many API differences between Python 2 and Python 3. By abstracting away the version differences, these libraries let you write most code in a uniform style while handling the discrepancies internally.

- **Feature Detection Rather than Version Checking:**  
  Instead of peppering your code with explicit Python version checks (e.g., `if sys.version_info < (3, 0):`), use feature detection (or “try/except” imports) to import the correct module or function. This often makes the code more maintainable. For example, for handling strings or iterators, detecting whether a functionality exists and falling back to an alternative can lead to a more resilient codebase.

- **Backport Needed Features:**  
  Sometimes, you may need to bring a modern Python feature to Python 2.7.5. Creating dedicated modules or even separate “backport packages” (which some communities use) encapsulates the differences. Make sure to document these well so that contributors know why the special cases exist.

---

### 2. Structure Your Code to Separate Modern and Legacy Code Paths

- **Organize into Submodules:**  
  Consider isolating parts of your code that are version-specific into submodules (e.g., a directory called `compat` or `backports`). Within this directory, you can provide separate implementations or shims that are conditionally imported based on the runtime environment.

- **Use Conditional Imports in Modules:**  
  For modules that differ between Python versions, conditional imports at the top of the module can import the correct implementation. For instance:

  ```python
  try:
      # Preferred implementation for Python 3.x
      from modern_module import function as my_function
  except ImportError:
      # Fallback for Python 2.x
      from legacy_module import function as my_function
  ```

- **Abstract Out Version-Specific Behaviors:**  
  Encapsulate version-dependent logic in helper functions so that the rest of your codebase can remain agnostic. This reduces duplication and isolates the compatibility logic.

---

### 3. Packaging and Dependency Management

- **Specify Python Version Requirements:**  
  In your `setup.py` or `pyproject.toml`, clearly declare your supported Python versions using `python_requires`. For example:
  
  ```python
  python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*'
  ```
  
  This helps pip decide which versions of your package to install and prevents installation on incompatible interpreters.

- **Use Conditional Dependencies:**  
  With PEP 508 environment markers, you can declare dependencies that should only be installed for specific Python versions. This is especially useful if you require additional backport libraries for Python 2.7, for example:

  ```python
  install_requires=[
      'some_modern_dependency',
      'backports.functools_lru_cache; python_version < "3.2"',
  ]
  ```

- **Separate Backport Packages:**  
  In some cases, you might choose to create separate packages (or use entry points) for Python 2.7 if the legacy support requires a significant divergence in behavior or additional dependencies. This approach can simplify maintenance by isolating the backport-specific code.

---

### 4. Testing Across All Supported Versions

- **Use Tox for Multi-Version Testing:**  
  Tox is a powerful tool for automating tests across multiple Python environments. By setting up a matrix of environments in your `tox.ini`, you ensure that both your modern and legacy code paths work as expected. For example:

  ```ini
  [tox]
  envlist = py27, py36, py37, py38, py39

  [testenv]
  deps =
      pytest
      six
      # Add any backport dependencies for Python 2.7 here
  commands =
      pytest
  ```

- **Continuous Integration (CI):**  
  Incorporate a CI service (such as GitHub Actions, Travis CI, or CircleCI) that runs your test suite against all supported Python versions. This helps catch regressions and ensures that any changes continue to work across your compatibility range.

---

### 5. Documentation and Community Communication

- **Document Compatibility Decisions:**  
  Clearly document in your README or developer guides why you’re supporting older versions, and list any known limitations or workarounds. This is crucial for open source contributors and users who rely on the package.

- **Encourage Community Contributions:**  
  The maintenance burden of backporting features can be mitigated by fostering a community that understands the challenges of supporting multiple Python versions. Encourage contributions specifically aimed at improving legacy support.

---

### 6. Keep Abreast of Community Best Practices

- **Monitor Evolving Best Practices:**  
  The Python ecosystem evolves, and best practices today may shift as more projects drop Python 2 support. Regularly check discussions in the Python Packaging Authority (PyPA), relevant PEPs, and community blogs. Even if your application must support Python 2.7 for now, planning an eventual transition is recommended.

- **Plan for the Future:**  
  At some point, maintaining support for Python 2.7 may no longer be practical. Make sure your roadmap accounts for a deprecation strategy where users are encouraged to upgrade their environments.

---

### Summary

For a modern package to support backports cleanly down to Python 2.7.5, you should:
- Employ compatibility libraries and conditional imports,
- Keep version-specific code isolated within dedicated modules,
- Clearly specify dependencies and Python version requirements during packaging,
- Set up automated multi-version testing with tools like Tox and CI,
- Document your choices and maintain a robust deprecation roadmap.

By following these steps, you ensure that your codebase remains maintainable, that you can catch issues through automated testing, and that end users on older Python versions have a seamless experience.