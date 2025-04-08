from setuptools import setup, find_packages

setup(
    name='iwalk',
    version='0.1.0',
    description='Drop-in replacement for os.walk() that respects .gitignore and other ignore files',
    author='',
    author_email='',
    url='',
    package_dir={{'': 'src'}},
    packages=find_packages(where='src'),
    python_requires='>=2.7, !=3.0.*, !=3.1.*',
    install_requires=[
        'pathspec>=0.5.9',
    ],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
)
