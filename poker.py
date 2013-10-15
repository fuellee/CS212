#! /usr/bin/env python
# -----------
# User Instructions
#
# Modify the hand_rank function so that it returns the
# correct output for the remaining hand types, which are:
# full house, flush, straight, three of a kind, two pair,
# pair, and high card hands.
#
# Do this by completing each return statement below.
#
# You may assume the following behavior of each function:
#
# straight(ranks): returns True if the hand is a straight.
# flush(hand):     returns True if the hand is a flush.
# kind(n, ranks):  returns the first rank that the hand has
#                  exactly n of. For A hand with 4 sevens
#                  this function would return 7.
# two_pair(ranks): if there is a two pair, this function
#                  returns their corresponding ranks as a
#                  tuple. For example, a hand with 2 twos
#                  and 2 fours would cause this function
#                  to return (4, 2).
# card_ranks(hand) returns an ORDERED tuple of the ranks
#                  in a hand (where the order goes from
#                  highest to lowest rank).
#
# Since we are assuming that some functions are already
# written, this code will not RUN. Clicking SUBMIT will
# tell you if you are correct.
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

def straight(ranks):
    "Return True if the ordered ranks form a 5-card straight."
    # return all([ranks[i]-ranks[i+1]==1 for i in range(len(ranks)-1)])
    return max(ranks)-min(ranks)==4 and len(ranks)==5 # ranks is sorted

def flush(hand):
    "Return True if all the cards have the same suit."
    return all([hand[i][1]==hand[i+1][1] for i in range(len(hand)-1)])
    suits = [s for r,s in hand]
    return len(set(suits))==1

def card_ranks(cards):
    "Return a list of the ranks, sorted with higher first."
    rank2num = {'A': 14, 'Q': 12, 'K': 13, 'J': 11, '1': 1, '3': 3, '2': 2, '5': 5, '4': 4, '7': 7, '6': 6, '9': 9, '8': 8, 'T': 10}
    ranks = [rank2num[r] for r,s in zip(*zip(*cards))]
    ranks.sort(reverse=True)
    return [5,4,3,2,1] if ranks==[14,5,4,3,2] else ranks  # no '1', and 'A' can be '1' or '14'

def kind(n, ranks):
    """Return the first rank that this hand has exactly n of.
    Return None if there is no n-of-a-kind in the hand."""
    # count2rank = {ranks.count(r):r for r in set(ranks)}
    # return count2rank.get(n,None)
    for r in ranks:
        if ranks.count(r)==n:
            return r
    return None

def two_pair(ranks):
    """If there are two pair, return the two ranks as a
    tuple: (highest, lowest); otherwise return None."""
    # pairs = tuple(ranks[i] for i in range(len(ranks)-1) if ranks[i]==ranks[i+1])
    # return pairs if len(pairs)==2 and pairs[0]!=pairs[1] else None
    pair = kind(2,ranks)
    lowpair = kind(2, list(reversed(ranks)))
    return (pair,lowpair) if pair and pair!=lowpair else None

def hand_rank(hand):
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):            # straight flush
        return (8, max(ranks))
    elif kind(4, ranks):                           # 4 of a kind
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):        # full house
        return (6,kind(3,ranks),kind(2,ranks))
    elif flush(hand):                              # flush
        return (5,ranks)
    elif straight(ranks):                          # straight
        return (4,max(ranks))
    elif kind(3, ranks):                           # 3 of a kind
        return (3,kind(3,ranks),ranks)
    elif two_pair(ranks):                          # 2 pair
        return (2,two_pair(ranks),ranks)
    elif kind(2, ranks):                           # kind
        return (1,kind(2,ranks), ranks)
    else:                                          # high card
        return (0,ranks)

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
    fkranks = card_ranks(fk)
    # tpranks = card_ranks(tp)
    kind(4, fkranks) == 9
    kind(3, fkranks) == None
    kind(2, fkranks) == None
    kind(1, fkranks) == 7
    assert hand_rank(sf) == (8, 10)
    assert hand_rank(fk) == (7, 9, 7)
    assert hand_rank(fh) == (6, 10, 7)
    assert straight(card_ranks(al)) == True
    assert poker([sf, fk, fh]) ==[sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh,fh]
    assert poker([sf]) == [sf]
    assert poker([sf] + 99*[fh]) == [sf]
    assert poker([sf1, sf2, fk, fh]) == [sf1, sf2]
    return 'tests pass'

# print test()
# hand_percentages(10000)
