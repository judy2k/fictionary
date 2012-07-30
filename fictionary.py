#!/usr/bin/env python

''' A random word generator, following standard English word rules.
'''

import logging

import argparse
from collections import Counter
from glob import glob
from os import makedirs
from os.path import join, exists
import random
import shelve
import sys

# Where to save the generated data file:
DATA_FILE_ROOT = './data'

# Where to load the source ispell wordlists:
SRC_DATA_FILE_ROOT = '.'


log = logging.getLogger(__name__)

ISPELL_FILESETS = {
    'all': glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/*.*')),
    'british': glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/english.*')) +
        glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/british.*')),
    'american': glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/english.*')) +
        glob(join(SRC_DATA_FILE_ROOT, 'ispell_wordlist/american.*')),
}


class Markov(object):
    ''' A markov chain, with 2-token tuples as keys. Values are implemented as Counter objects, providing 
    '''
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
        ''' Obtain a weighted, random token, transitioning from the current state (key).
        
        Given the provided key (current state), provide a randomly-generated
        state using the model's weighted collection of next states.
        '''
        log.debug('Key: %r, Counters: %r', key, self[key])
        return random_choice(self[key])

    def random_sequence(self, min_length=4):
        while True:
            result = list(self._random_sequence())
            if len(result) >= min_length:
                return result
    
    def _random_sequence(self):
        key = (None, None)
        while True:
            next = self.next(key)
            if not next:
                return
            else:
                yield next
                key = (key[1], next)


def pick(counter, i):
    ''' Pick a key from Counter, using the key's count as a weighting.
    
    This function sorts counter contents in order of count, and uses each
    count as a range providing a weighting for the associated value. The
    parameter `i` provides an index into one of the ranges, and that count's
    associated key is returned.
    '''
    total = 0
    for val, count in counter.most_common():
        total += count
        if i < total:
            return val
    raise IndexError('Value of i (%d) was greater than max index (%d)' % (i, sum(counter.values())-1))


def random_choice(counter, weighted=True):
    ''' Obtain a randomly-chosen key from the provided counter.
    
    If weighted is True, the key returned is weighted by its associated count,
    so keys with a high count value should be chosen more frequently. If
    weighted is False, the keys in counter are treated as a flat list, and
    each has the same probability of being chosen.
    '''
    if weighted:
        return pick(counter, random.randint(0, sum(counter.values())-1))
    else:
        return random.choice(counter.most_common())[0]


def generate_word_list(files):
    ''' Read through one or more wordlist files and generate a Markov object representing the words.
    
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
    

def main(argv=sys.argv[1:]):
    ap = argparse.ArgumentParser()
    ap.add_argument('-v', '--verbose', action='store_true', help="Be verbose.")
    ap.add_argument('-c', '--count', type=int, default=1, help="The number of words to generate.")
    ap.add_argument('-m', '--min-length', type=int, default=4, metavar="MIN", help="Only generate words of MIN length or longer.")
    ap.add_argument('--refresh', action='store_true', help="Re-create the data file from the word-lists.")
    ap.add_argument('-d', '--dictionary', default='british', help="The dictionary rules to follow")

    args = ap.parse_args(argv)

    if args.verbose:
        logging.basicConfig()
        log.setLevel(logging.DEBUG)

    data_file_path = join(DATA_FILE_ROOT, 'dictionary.dat')
    if not exists(data_file_path) or args.refresh:
        try:
            if not exists(DATA_FILE_ROOT):
                makedirs(DATA_FILE_ROOT)
            shelf = shelve.open(data_file_path, protocol=2, flag='n')
            for dictionary in ['all', 'british', 'american']:
                print "Generating '%s' dictionary... " % dictionary,
                shelf[dictionary] = generate_word_list(ISPELL_FILESETS[dictionary])
                print 'Done.'
        finally:
            try:
                shelf.sync()
            except Exception: pass
    else:
        shelf = shelve.open(data_file_path, protocol=2, flag='w')

    model = shelf[args.dictionary]

    for _ in range(args.count):
        print ''.join(model.random_sequence(args.min_length))


if __name__ == '__main__':
    main()