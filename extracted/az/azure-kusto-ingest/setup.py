# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License

import re
from os import path

from setuptools import setup, find_packages

PACKAGE_NAME = "azure-kusto-ingest"

# a-b-c => a/b/c
PACKAGE_FOLDER_PATH = PACKAGE_NAME.replace("-", path.sep)
# a-b-c => a.b.c
NAMESPACE_NAME = PACKAGE_NAME.replace("-", ".")

with open(path.join(PACKAGE_FOLDER_PATH, "_version.py"), "r") as fd:
    VERSION = re.search(r'^VERSION\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not VERSION:
    raise RuntimeError("Cannot find version information")

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="Kusto Ingest Client",
    long_description_content_type="text/markdown",
    long_description=open("README.rst", "r").read(),
    license="MIT",
    author="Microsoft Corporation",
    author_email="kustalk@microsoft.com",
    url="https://github.com/Azure/azure-kusto-python",
    namespace_packages=["azure"],
    classifiers=[
        # 5 - Production/Stable depends on multi-threading / aio / perf
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
    ],
    packages=find_packages(exclude=["azure", "*tests*", "*tests.*"]),
    package_data={"": ["py.typed"]},
    install_requires=[
        "azure-kusto-data=={}".format(VERSION),
        # TODO - this has to be locked to this version due to https://github.com/Azure/azure-sdk-for-python/issues/40041
        "azure-storage-blob==12.23.0",
        "azure-storage-queue==12.12.0",
        "tenacity>=8.0.0",
    ],
    extras_require={"pandas": ["pandas"], "aio": []},
)
