# installation: pip install nested-lookup

from setuptools import setup, find_packages


# get list of requirement strings from requirements.txt
def remove_whitespace(x):
    return "".join(x.split())


def sanitize(x):
    return not x.startswith("#") and x != ""


def requirements():
    with open("requirements.txt", "r") as f:
        r = f.readlines()
    map(remove_whitespace, r)
    filter(sanitize, r)
    return r

print(requirements())

setup(
    name="nested-lookup",
    version="0.2.25",
    description="Python functions for working with deeply nested documents (lists and dicts) ",
    keywords="nested document dictionary dict list lookup schema json xml yaml",
    long_description=open("README.rst").read(),
    author="Russell Ballestrini",
    author_email="russell.ballestrini@gmail.com",
    url="https://git.unturf.com/python/nested-lookup",
    platforms=["All"],
    license="Public Domain",
    packages=find_packages(exclude="tests"),
    include_package_data=True,
    install_requires=requirements(),
    classifiers=[
        # this library supports the following Python versions.
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)

# setup keyword args: http://peak.telecommunity.com/DevCenter/setuptools

# build package:
# pip install twine
# python setup.py sdist
# twine upload dist/*
