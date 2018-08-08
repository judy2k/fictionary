#!/usr/bin/env python

import sys

from setuptools import setup

setup(
    name="fictionary",
    version="0.0.4",
    description="Generate made-up words following the patterns used by real"
                " English words.",
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
    ],
    keywords="words dictionary fictionary",

    packages=['fictionary'],
    package_dir={"": "src"},
    package_data={
        'fictionary': ['ispell_wordlist/*']
    },
    install_requires=[],
    zip_safe=False,

    entry_points={
        'console_scripts': [
            'fictionary=fictionary:main',
        ]
    },
)
