#!/usr/bin/env python

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

REQUIREMENTS = [
    "click>=5.0,<6.0",
],

TEST_REQUIREMENTS = [
    "pytest>=2.7.2",
    "pbr<1.7.0",        # There appears to be a problem with tox & pbr==1.7.0
    "mock>=1.3.0",
]


class PyTest(TestCommand):
    user_options = []

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name="fictionary",
    version="0.0.2",
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
    package_data={
        'fictionary': ['ispell_wordlist/*']
    },
    install_requires=REQUIREMENTS,
    zip_safe=False,

    entry_points={
        'console_scripts': [
            'fictionary=fictionary:main',
        ]
    },

    cmdclass={'test': PyTest},
    tests_require=TEST_REQUIREMENTS,
)
