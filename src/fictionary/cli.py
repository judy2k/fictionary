""" A made-up word factory, following standard English word rules.
"""

from __future__ import print_function, unicode_literals

import argparse
import logging
import os.path
import sys

import click

import fictionary
import fictionary.model

LOG = logging.getLogger("fictionary.cli")

# Where to save the generated data file:

DATA_FILE_ROOT = click.get_app_dir(fictionary.APP_NAME)


def main(argv=sys.argv[1:]):
    """
    Entry-function for running fictionary as a command-line program.
    """
    try:
        parser = argparse.ArgumentParser(description=__doc__.strip())
        parser.add_argument("-v", "--verbose", action="store_true", help="Be verbose.")
        parser.add_argument(
            "-c",
            "--count",
            type=int,
            default=fictionary.DEFAULT_NUM_WORDS,
            help="The number of words to make_model.",
        )
        parser.add_argument(
            "-m",
            "--min-length",
            type=int,
            default=fictionary.model.DEFAULT_MIN_LENGTH,
            metavar="LENGTH",
            help="Only make_model words of LENGTH chars or longer.",
        )
        parser.add_argument(
            "-x",
            "--max-length",
            type=int,
            default=None,
            metavar="LENGTH",
            help="Only make_model words of LENGTH chars or shorter.",
        )
        parser.add_argument(
            "-d",
            "--dictionary",
            default=fictionary.DICT_BRITISH_KEY,
            help="The dictionary rules to follow: american, british, or all",
        )

        args = parser.parse_args(argv)

        if args.max_length is not None:
            if args.min_length > args.max_length:
                print(
                    "Words cannot have a max-length shorter than their min-length!",
                    file=sys.stderr,
                )
                return -1

        logging.basicConfig(
            level=logging.DEBUG if args.verbose else logging.WARNING,
            format="%(message)s",
        )

        random_words = fictionary.get_random_words(
            num_words=args.count,
            min_length=args.min_length,
            max_length=args.max_length,
            dictionary=args.dictionary,
        )

        for word in random_words:
            print(word)
    except KeyboardInterrupt:
        pass

    return 0
