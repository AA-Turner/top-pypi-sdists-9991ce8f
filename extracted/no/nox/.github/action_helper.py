from __future__ import annotations

import json
import sys


def filter_version(version: str) -> str:
    """return python 'major.minor'"""

    # remove interpreter prefix
    if version.startswith("pypy-"):
        version_ = version[5:]
    elif version.startswith("pypy"):
        version_ = version[4:]
    elif version.startswith("~"):
        version_ = version[1:]
    else:
        version_ = version

    # remove extra specifier e.g. "3.12-dev" => "3.12", "~3.12.0-0" => "3.12"
    version_ = version_.split("-")[0]

    version_parts = version_.split(".")
    if len(version_parts) < 2:
        msg = f"invalid version: {version}"
        raise ValueError(msg)
    if not version_parts[0].isdigit():
        msg = f"invalid major python version: {version}"
        raise ValueError(msg)
    if not version_parts[1].isdigit():
        msg = f"invalid minor python version: {version}"
        raise ValueError(msg)
    return ".".join(version_parts[:2])


def setup_action(input_: str, *, self_version: str = "3.12") -> None:
    versions = [version.strip() for version in input_.split(",") if version.strip()]

    pypy_versions = [version for version in versions if version.startswith("pypy")]
    pypy_versions_filtered = [filter_version(version) for version in pypy_versions]
    if len(pypy_versions) != len(set(pypy_versions_filtered)):
        msg = (
            "multiple versions specified for the same 'major.minor' PyPy interpreter:"
            f" {pypy_versions}"
        )
        raise ValueError(msg)

    cpython_versions = [version for version in versions if version not in pypy_versions]
    cpython_versions_filtered = [
        filter_version(version) for version in cpython_versions
    ]
    if len(cpython_versions) != len(set(cpython_versions_filtered)):
        msg = (
            "multiple versions specified for the same 'major.minor' CPython"
            f" interpreter: {cpython_versions}"
        )
        raise ValueError(msg)

    # cpython shall be installed last because
    # other interpreters also define pythonX.Y symlinks.
    versions = pypy_versions + cpython_versions

    # we want to install our own self version last to ease nox set-up
    if self_version in cpython_versions_filtered:
        index = cpython_versions_filtered.index(self_version)
        index = versions.index(cpython_versions[index])
        cpython_nox = versions.pop(index)
        versions.append(cpython_nox)
    else:
        # add this to install nox
        versions.append(self_version)

    print(f"interpreters={json.dumps(versions)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        msg = f"invalid arguments: {sys.argv}"
        raise AssertionError(msg)
    setup_action(sys.argv[1])
