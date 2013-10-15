#! /usr/bin/env python
# code form https://www.udacity.com/wiki/cs212/unit_1_code
# shuffers and tests
import random
from collections import defaultdict

def factorial(n): return 1 if (n <= 1) else n*factorial(n-1)

def shuffle1(deck):
    # O(N**2)
    # incorrect distribution
    N = len(deck)
    swapped = [False] * N
    while not all(swapped):
        i, j = random.randrange(N), random.randrange(N)
        swapped[i] = swapped[j] = True
        deck[i], deck[j] = deck[j], deck[i]

def shuffle2(deck):
    # O(N**2)
    # incorrect distribution?
    N = len(deck)
    swapped = [False] * N
    while not all(swapped):
        i, j = random.randrange(N), random.randrange(N)
        swapped[i] = True
        deck[i], deck[j] = deck[j], deck[i]

def shuffle2a(deck):
    # http://forums.udacity.com/cs212-april2012/questions/3462/better-implementation-of-shuffle2
    N = len(deck)
    swapped = [False] * N
    while not all(swapped):
        i = random.choice(filter(lambda idx: not swapped[idx], range(N)))
        j = random.choice(filter(lambda idx: not swapped[idx], range(N)))
        swapped[i] = True
        deck[i], deck[j] = deck[j], deck[i]

def shuffle3(deck):
    # O(N)
    # incorrect distribution
    N = len(deck)
    for i in range(N):
        j = random.randrange(N)
        deck[i], deck[j] = deck[j], deck[i]

def shuffle(deck):
    # Knuth method
    n = len(deck)
    for i in range(n-1):
        j = random.randrange(i, n)
        deck[i], deck[j] = deck[j], deck[i]

def test_shuffler(shuffler, deck='abcd', n=10000):
    counts = defaultdict(int)
    for _ in range(n):
        input = list(deck)
        shuffler(input)
        counts[''.join(input)] += 1
    e = n*1./factorial(len(deck))  ## expected count
    ok = all((0.9 <= counts[item]/e <= 1.1) for item in counts)
    name = shuffler.__name__
    print '%s(%s) %s' % (name, deck, ('ok' if ok else '*** bad ***'))
    print '    ',
    for item, count in sorted(counts.items()):
        print "%s:%4.1f" % (item, count*100./n),
    print

def test_shufflers(shufflers=[shuffle, shuffle1, shuffle2, shuffle3], decks=['abc','ab']):
    for deck in decks:
        print
        for f in shufflers:
            test_shuffler(f, deck)

print test_shufflers()
