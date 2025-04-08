import sys

if sys.version_info < (3, 0):
    from .compat.py27.iwalk import walk
elif sys.version_info < (3, 3):
    from .compat.py32.iwalk import walk  # Placeholder for future Python 3.2 support
else:
    from .compat.py39.iwalk import walk
