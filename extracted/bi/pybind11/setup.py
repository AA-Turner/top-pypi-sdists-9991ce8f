#!/usr/bin/env python3

# Setup script (in the sdist or in tools/setup_main.py in the repository)

from setuptools import setup

cmdclass = {}


setup(
    name="pybind11",
    version="2.13.6",
    download_url='https://github.com/pybind/pybind11/tarball/v2.13.6',
    packages=[
        "pybind11",
        "pybind11.include.pybind11",
        "pybind11.include.pybind11.detail",
        "pybind11.include.pybind11.eigen",
        "pybind11.include.pybind11.stl",
        "pybind11.share.cmake.pybind11",
        "pybind11.share.pkgconfig",
    ],
    package_data={
        "pybind11": ["py.typed"],
        "pybind11.include.pybind11": ["*.h"],
        "pybind11.include.pybind11.detail": ["*.h"],
        "pybind11.include.pybind11.eigen": ["*.h"],
        "pybind11.include.pybind11.stl": ["*.h"],
        "pybind11.share.cmake.pybind11": ["*.cmake"],
        "pybind11.share.pkgconfig": ["*.pc"],
    },
    extras_require={
        "global": ["pybind11_global==2.13.6"]
        },
    entry_points={
        "console_scripts": [
             "pybind11-config = pybind11.__main__:main",
        ],
        "pipx.run": [
             "pybind11 = pybind11.__main__:main",
        ]
    },
    cmdclass=cmdclass
)
