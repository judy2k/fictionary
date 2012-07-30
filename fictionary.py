import argparse
from collections import Counter
from glob import glob
from os.path import join
import sys

DATA_FILE_ROOT = '.'
ISPELL_FILESETS = {
    'all': glob(join(DATA_FILE_ROOT, 'ispell_wordlist/*.*')),
    'british': glob(join(DATA_FILE_ROOT, 'ispell_wordlist/english.*')) +
        glob(join(DATA_FILE_ROOT, 'ispell_wordlist/british.*')),
    'american': glob(join(DATA_FILE_ROOT, 'ispell_wordlist/english.*')) +
        glob(join(DATA_FILE_ROOT, 'ispell_wordlist/american.*')),
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

    def __getitem__(key):
        return self.data[key]

def generate_word_list(files):
    result = Markov()
    for path in files:
        for line in open(path):
            if not line[0].isupper() and "'" not in line:
                print line.strip()
                result.feed(line.strip())
    return result


def main(argv=sys.argv[1:]):
    print 'Running'
    m = generate_word_list(ISPELL_FILESETS['british'])
    import pprint
    
    
                
if __name__ == '__main__':
    main()