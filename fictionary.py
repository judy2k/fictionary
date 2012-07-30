#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' A made-up word factory, following standard English word rules.
'''

import sys

try:
    from collections import Counter
except ImportError:
    print >> sys.stderr, "You need Python >= 2.7 to run fictionary."
    sys.exit(-1)

import argparse
from glob import glob
import logging
from os import makedirs
from os.path import join, exists, basename
import random
import shelve

# Where to save the generated data file:
DATA_FILE_ROOT = './data'

# Where to load the source ispell wordlists:
SRC_DATA_FILE_ROOT = '.'


LOG = logging.getLogger(__name__)

ISPELL_FILESETS = {
    'all': glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/*.*')),
    'british': glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/english.*')) +
    glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/british.*')),
    'american': glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/english.*')) +
    glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/american.*')),
}


class Markov(object):
    ''' A markov chain, with 2-token tuples as keys.

    Values are implemented as Counter objects, providing a weighting for each
    successive token.
    '''
    def __init__(self):
        self.data = {}

    def feed(self, tokens):
        ''' Add a sequence of tokens for addition to the Markov model. '''
        terms = [None, None] + list(tokens) + [None]
        for index in range(len(terms) - 2):
            pair = tuple(terms[index:index + 2])
            nxt = terms[index + 2]
            options = self.data.get(pair, None)
            if options is not None:
                options.update([nxt])
            else:
                options = RandomCounter([nxt])
                self.data[pair] = options

    def __getitem__(self, key):
        return self.data[key]

    def random_sequence(self, min_length=4, max_length=None):
        ''' Generate a random sequence from the Markov model.

        Any resulting sequences which are shorter than min_length (which
        defaults to 4) are filtered out.
        '''
        for _ in range(1000):
            result = list(self.random_sequence_generator())
            if (len(result) >= min_length
                and (max_length is None or len(result) <= max_length)):
                LOG.debug('Result: %s (%d <= %d <= %r)', result, min_length, len(result), max_length)
                return result
        else:
            raise Exception("Couldn't find a valid word in 1000 iterations - "
                            "it looks like something is wrong!")

    def random_sequence_generator(self):
        ''' A generator to provide a sequence from the Markov model. '''
        key = (None, None)
        while True:
            next_token = self[key].random_choice()
            if not next_token:
                return
            else:
                yield next_token
                key = (key[1], next_token)


class RandomCounter(Counter):
    ''' A Counter with extra methods for choosing random keys from the
    collection, accounting for weightings provided by the counter values.
    '''
    def pick(self, i):
        ''' Pick a key from Counter, using the key's count as a weighting.

        This function sorts counter contents in order of count, and uses each
        count as a range providing a weighting for the associated value. The
        parameter `i` provides an index into one of the ranges, and that
        count's associated key is returned.
        '''
        total = 0
        for val, count in self.most_common():
            total += count
            if i < total:
                return val
        raise IndexError('Value of i (%d) was greater than max index (%d)'
                         % (i, sum(self.values()) - 1))

    def random_choice(self, weighted=True):
        ''' Obtain a randomly-chosen key from the counter.

        If weighted is True, the key returned is weighted by its associated
        count, so keys with a high count value should be chosen more
        frequently.  If weighted is False, the keys in counter are treated as
        a flat list, and each has the same probability of being chosen.
        '''
        if weighted:
            return self.pick(random.randint(0, sum(self.values()) - 1))
        else:
            return random.choice(self.most_common())[0]


def generate_word_list(files):
    '''
    Read through one or more wordlist files and generate a Markov object
    representing the words.

    ``files`` should be a sequence of file paths. Each file will be opened, and
    each line should contain a single word.  Words beginning with a capital
    letter or containing an apostrophe will be rejected. Each word is fed into
    a Markov object as a sequence of characters.
    '''
    result = Markov()
    for path in files:
        for line in open(path):
            if not line[0].isupper() and "'" not in line:
                result.feed(line.strip())
    return result


def open_data_file(data_file_path, filesets, force_refresh):
    '''
    Open a fictionary data file, creating a new one if necessary, or if
    ``force_refresh`` is True.
    '''
    if force_refresh or not exists(data_file_path):
        return generate_data_file(data_file_path, filesets)
    else:
        return shelve.open(data_file_path, protocol=2, flag='w')


def generate_data_file(data_file_path, filesets):
    '''
    Create a new fictionary data file at ``data_file_path`` from the files
    listed in ``filesets``
    '''
    containing_dir = basename(data_file_path)
    if not exists(containing_dir):
        makedirs(containing_dir)
    shelf = shelve.open(data_file_path, protocol=2, flag='n')
    for dictionary in ['all', 'british', 'american']:
        print "Generating '%s' dictionary... " % dictionary,
        shelf[dictionary] = generate_word_list(filesets[dictionary])
        print 'Done.'
    return shelf


def main(argv=sys.argv[1:]):
    """
    Entry-function for running fictionary as a command-line program.
    """
    parser = argparse.ArgumentParser(description=__doc__.strip())
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Be verbose.")
    parser.add_argument('-c', '--count', type=int, default=1,
                        help="The number of words to generate.")
    parser.add_argument('-m', '--min-length', type=int, default=4,
                        metavar="LENGTH",
                        help="Only generate words of LENGTH chars or longer.")
    parser.add_argument('-x', '--max-length', type=int, default=None,
                        metavar="LENGTH",
                        help="Only generate words of LENGTH chars or shorter.")
    parser.add_argument('--refresh', action='store_true',
                        help="Re-create the data file from the word-lists.")
    parser.add_argument('-d', '--dictionary', default='british',
                        help="The dictionary rules to follow: american,"
                        "british, or all")

    args = parser.parse_args(argv)

    if args.max_length is not None:
        if args.min_length > args.max_length:
            print >> sys.stderr, "Words cannot have a max-length shorter than their min-length!"
            sys.exit(-1)

    if args.verbose:
        logging.basicConfig()
        LOG.setLevel(logging.DEBUG)

    shelf = open_data_file(join(DATA_FILE_ROOT, 'dictionary.dat'),
                           ISPELL_FILESETS, args.refresh)
    model = shelf[args.dictionary]
    for _ in range(args.count):
        print ''.join(model.random_sequence(args.min_length, args.max_length))


if __name__ == '__main__':
    main()
