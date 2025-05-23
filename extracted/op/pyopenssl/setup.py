#!/usr/bin/env python
#
# Copyright (C) Jean-Paul Calderone 2008-2015, All rights reserved
#

"""
Installation script for the OpenSSL package.
"""

import os
import re

from setuptools import find_packages, setup

HERE = os.path.abspath(os.path.dirname(__file__))
META_PATH = os.path.join("src", "OpenSSL", "version.py")


def read_file(*parts):
    """
    Build an absolute path from *parts* and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    with open(os.path.join(HERE, *parts), encoding="utf-8", newline=None) as f:
        return f.read()


META_FILE = read_file(META_PATH)


def find_meta(meta):
    """
    Extract __*meta*__ from META_FILE.
    """
    meta_match = re.search(
        rf"^__{meta}__ = ['\"]([^'\"]*)['\"]", META_FILE, re.M
    )
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError(f"Unable to find __{meta}__ string.")


URI = find_meta("uri")
LONG = (
    read_file("README.rst")
    + "\n\n"
    + "Release Information\n"
    + "===================\n\n"
    + re.search(
        r"(\d{2}.\d.\d \(.*?\)\n.*?)\n\n\n----\n",
        read_file("CHANGELOG.rst"),
        re.S,
    ).group(1)
    + "\n\n`Full changelog "
    + "<{uri}en/stable/changelog.html>`_.\n\n"
).format(uri=URI)


if __name__ == "__main__":
    setup(
        name=find_meta("title"),
        version=find_meta("version"),
        description=find_meta("summary"),
        long_description=LONG,
        author=find_meta("author"),
        author_email=find_meta("email"),
        url=URI,
        project_urls={
            "Source": "https://github.com/pyca/pyopenssl",
        },
        license=find_meta("license"),
        classifiers=[
            "Development Status :: 6 - Mature",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Security :: Cryptography",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: System :: Networking",
        ],
        python_requires=">=3.7",
        packages=find_packages(where="src"),
        package_dir={"": "src"},
        install_requires=[
            "cryptography>=41.0.5,<46",
            (
                "typing-extensions>=4.9; "
                "python_version < '3.13' and python_version >= '3.8'"
            ),
        ],
        extras_require={
            "test": ["pytest-rerunfailures", "pretend", "pytest>=3.0.1"],
            "docs": [
                "sphinx!=5.2.0,!=5.2.0.post0,!=7.2.5",
                "sphinx_rtd_theme",
            ],
        },
    )
