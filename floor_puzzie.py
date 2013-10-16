#! /usr/bin/env python
#------------------
# User Instructions
#
# Hopper, Kay, Liskov, Perlis, and Ritchie live on
# different floors of a five-floor apartment building.
#
# Hopper does not live on the top floor.
# Kay does not live on the bottom floor.
# Liskov does not live on either the top or the bottom floor.
# Perlis lives on a higher floor than does Kay.
# Ritchie does not live on a floor adjacent to Liskov's.
# Liskov does not live on a floor adjacent to Kay's.
#
# Where does everyone live?
#
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay,
# Liskov, Perlis, and Ritchie.

import itertools

orderings = itertools.permutations([1,2,3,4,5])

def floor_puzzle():
    # Your code here
    return [(Hopper, Kay, Liskov, Perlis, Ritchie)
            for (Hopper, Kay, Liskov, Perlis, Ritchie) in orderings
            if Hopper!=5       # Hopper does not live on the top floor.
               and Kay!=1      # Kay does not live on the bottom floor.
               and Liskov!=5 and Liskov!=1 # Liskov does not live on either the top or the bottom floor.
               and Perlis>Kay  # Perlis lives on a higher floor than does Kay.
               and abs(Ritchie-Liskov)!=1 # Ritchie does not live on a floor adjacent to Liskov's.
               and abs(Liskov-Kay)!=1 # Liskov does not live on a floor adjacent to Kay's.
            ]

print floor_puzzle()
