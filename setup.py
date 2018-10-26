#!/usr/bin/env python

import io
from setuptools import setup, find_packages

from os import path

this_directory = path.abspath(path.dirname(__file__))
with io.open(path.join(this_directory, "README.rst"), encoding="utf-8") as fp:
    long_description = fp.read()

setup(
    name="fictionary",
    version="0.1.0",
    description="Generate made-up words following the patterns used by real"
    " English words.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/judy2k/fictionary",
    author="Mark Smith",
    author_email="mark.smith@practicalpoetry.co.uk",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords="words dictionary fictionary",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"fictionary": ["models/*.txt"]},
    install_requires=[],
    zip_safe=False,
    entry_points={"console_scripts": ["fictionary=fictionary.cli:main"]},
)
