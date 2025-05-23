from setuptools import setup

setup(
    name="dacite",
    version="1.9.2",
    description="Simple creation of data classes from dictionaries.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Konrad Hałas",
    author_email="halas.konrad@gmail.com",
    url="https://github.com/konradhalas/dacite",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="dataclasses",
    packages=["dacite"],
    package_data={"dacite": ["py.typed"]},
    install_requires=['dataclasses;python_version<"3.7"'],
    extras_require={
        "dev": ["pytest>=5", "pytest-benchmark", "pytest-cov", "coveralls", "black", "mypy", "pylint", "pre-commit"]
    },
)
