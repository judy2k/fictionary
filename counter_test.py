import random
from collections import Counter

class Chooser(object):
    def __init__(self):
        self.c = Counter()
        input = list('abcdefghijabcdefghabcdefabcabcabaaaaa')
        random.shuffle(input)
        self.c.update(input)
        print 'sum: %d' % sum(self.c.values())
    
    def random_choice(weighted=True):
        if weighted:
            return self.pick(random.randint(0, self.count_sum-1))
        else:
            return random.choice(self.c.most_common())[0]
    
    @property
    def count_sum(self):
        return sum(self.c.values())
    
    def pick(self, i):
        total = 0
        for val, count in self.c.most_common():
            total += count
            if i < total:
                return val
        raise IndexError('Value of i (%d) was greater than max index (%d)' % (i, self.count_sum-1)

c = Chooser()

for i in range(40):
    c.random_choice()