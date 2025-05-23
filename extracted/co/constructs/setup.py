import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "constructs",
    "version": "10.4.2",
    "description": "A programming model for software-defined state",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/constructs",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services<aws-cdk-dev@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws/constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "constructs",
        "constructs._jsii"
    ],
    "package_data": {
        "constructs._jsii": [
            "constructs@10.4.2.jsii.tgz"
        ],
        "constructs": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "jsii>=1.102.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
