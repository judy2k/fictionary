#!/usr/bin/env python
import logging

log = logging.getLogger(__name__)

import argparse
from collections import Counter
from glob import glob
from os import makedirs
from os.path import join, exists
import random
import shelve
import sys

DATA_FILE_ROOT = './data'
SRC_DATA_FILE_ROOT = '.'
ISPELL_FILESETS = {
    'all': glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/*.*')),
    'british': glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/english.*')) +
        glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/british.*')),
    'american': glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/english.*')) +
        glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/american.*')),
}


class Markov(object):
    def __init__(self):
        self.data = {}

    def feed(self, tokens):
        terms = [None, None] + list(tokens) + [None]
        for index in range(len(terms)-2):
            pair = tuple(terms[index:index+2])
            nxt = terms[index+2]
            options = self.data.get(pair, None)
            if options is not None:
                options.update([nxt])
            else:
                options = Counter([nxt])
                self.data[pair] = options

    def __getitem__(self, key):
        return self.data[key]

    def next(self, key):
        log.debug('Key: %r, Counters: %r', key, self[key])
        return random_choice(self[key])

    def random_sequence(self):
        key = (None, None)
        result = []
        while True:
            next = self.next(key)
            if not next:
                return result
            else:
                result.append(next)
                key = (key[1], next)


def pick(counter, i):
    total = 0
    for val, count in counter.most_common():
        total += count
        if i < total:
            return val
    raise IndexError('Value of i (%d) was greater than max index (%d)' % (i, sum(counter.values())-1))


def random_choice(counter, weighted=True):
    if weighted:
        return pick(counter, random.randint(0, sum(counter.values())-1))
    else:
        return random.choice(counter.most_common())[0]


def generate_word_list(files):
    result = Markov()
    for path in files:
        for line in open(path):
            if not line[0].isupper() and "'" not in line:
                result.feed(line.strip())
    return result


def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument('-v', '--verbose', action='store_true', help="Be verbose.")
    ap.add_argument('-c', '--count', type=int, default=1, help="The number of words to generate.")

    args = ap.parse_args(argv)

    if args.verbose:
        logging.basicConfig()
        log.setLevel(logging.DEBUG)

    data_file_path = join(DATA_FILE_ROOT, 'dictionary.dat')
    if exists(data_file_path):
        shelf = shelve.open(data_file_path, protocol=2, flag='w')
    else:
        print 'Generating initial dictionary... ',
        try:
            shelf = shelve.open(data_file_path, protocol=2)
            m = generate_word_list(ISPELL_FILESETS['british'])
            makedirs(DATA_FILE_ROOT)
            shelf['british'] = m
        finally:
            try:
                shelf.close()
            except Exception: pass
        print 'Done.'

    model = shelf['british']

    for _ in range(args.count):
        print ''.join(model.random_sequence())


if __name__ == '__main__':
    main()