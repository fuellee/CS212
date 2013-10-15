#! /usr/bin/env python
# refactor the hand_rank function:
# -----------
# hand_rank,straight,flush,kind,two_pair,card_ranks
# => hand_rank,group,unzip
import random
hand_names = ['High Card',
              'Pair',
              '2 Pair',
              '3 Kind',
              'Straight',
              'Flush',
              'Full House',
              '4 kind',
              'Straight Flush']
mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

def hand_rank(hand):
    "Return a value indicating how high the hand ranks."
    # counts is the count of each rank; ranks list corressponding ranks
    # E.g. '7 T 7 9 7' => counts = (3,1,1); ranks = (7,10,9)
    groups = group(['--23456789TJQKA'.index(r) for r,s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14,5,4,3,2):
        ranks = (5,4,3,2,1)

    straight = len(ranks)==5 and max(ranks)-min(ranks)==4  # ...
    flush = len(set([s for r,s in hand]))==1

    # partition of 5 in lexicographic order, each has a name in poker game
    return (9 if (5,)==counts else
            8 if straight and flush else
            7 if (4,1)==counts else
            6 if (3,2)==counts else
            5 if flush else
            4 if straight else
            3 if (3,1,1)==counts else
            2 if (2,2,1)==counts else
            1 if (2,1,1,1)==counts else
            0), ranks

def group(items):
    "Return a list of [(count, x)...],highest count first, then highest x first."
    groups = [(items.count(x), x) for x in set(items)]
    return sorted(groups, reverse=True)

def unzip(pairs):
    "list of pairs => pair of lists"
    return zip(*pairs)

def poker(hands):
    "Return a list of winning hands: poker([hand,...]) => [hand,...]"
    return allmax(hands, key=hand_rank)

def allmax(iterable, key=None):
    "Return a list of all items equal to the max of the iterable."
    if key==None:key=lambda x:x
    result, maxval = [],None
    for x in iterable:
        xval = key(x)
        if result is [] or xval>maxval:
            result, maxval = [x],xval
        elif xval==maxval:
            result.append(x)
    return result

def deal(numhands, n=5, deck=[r+s for r in '23456789TJQKA' for s in 'SHDC']):
    "Shuffle the deck and deal out numhands n-card hands."
    random.shuffle(mydeck)
    return [mydeck[i*n:(i+1)*n] for i in range(numhands)]

def hand_percentages(n=700000):
    "Sample n random hands and print a table of precentages for each type of hand."
    counts = [0]*9
    for i in range(n/10):
        for hand in deal(10):
            ranking = hand_rank(hand)[0]
            counts[ranking]+=1
    for i in reversed(range(9)):
        print "%14s: %6.3f %%"%(hand_names[i],100.*counts[i]/n)


def test():
    "Test cases for the functions in poker program"
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    sf1 = "6C 7C 8C 9C TC".split() # Straight Flush
    sf2 = "6D 7D 8D 9D TD".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full Hous
    al = "AC 2D 4H 3D 5S".split() # Ace-Low Straight
    assert hand_rank(sf)[0]== 8
    assert hand_rank(fk)[0] == 7
    assert hand_rank(fh)[0] == 6
    assert poker([sf, fk, fh]) ==[sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh,fh]
    assert poker([sf]) == [sf]
    assert poker([sf] + 99*[fh]) == [sf]
    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2]
    return 'tests pass'

print test()
# hand_percentages(10000)
