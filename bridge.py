#! /usr/bin/env python
# -----------------
# User Instructions
#
# Write a function, bsuccessors(state), that takes a state as input
# and returns a dictionary of {state:action} pairs.
#
# A state is a (here, there, t) tuple, where here and there are
# frozensets of people (indicated by their times), and potentially
# the 'light,' t is a number indicating the elapsed time.
#
# An action is a tuple (person1, person2, arrow), where arrow is
# '->' for here to there or '<-' for there to here. When only one
# person crosses, person2 will be the same as person one, so the
# action (2, 2, '->') means that the person with a travel time of
# 2 crossed from here to there alone.

import itertools
# state:: (here, there, total_time)
# bsuccessors :: state -> {state:action}
def bsuccessors(state):
    """Return a dict of {state:action} pairs. A state is a (here, there, t) tuple,
    where here and there are frozensets of people (indicated by their times) and/or
    the 'light', and t is a number indicating the elapsed time. Action is represented
    as a tuple (person1, person2, arrow), where arrow is '->' for here to there and
    '<-' for there to here."""
    here, there, t = state
    # your code here
    successors = {}
    (from_, to, arrow) = (here,there,'->') if 'light' in here else (there,here,'<-')

    for (person1,person2) in itertools.combinations_with_replacement(from_-{'light'} ,2):
        team = {person1, person2, 'light'}
        _from_ = from_ - team
        _to   = to | team
        total_time = t+max(person1,person2)

        state = (_from_, _to, total_time) if arrow is '->' else (_to, _from_, total_time)
        action = (person1, person2, arrow)
        successors[state]=action
    return successors

# best first search
def bridge_problem(here):
    here = frozenset(here) | {'light'}
    explored = set()
    frontier = [ [(here, frozenset(), 0)]]  # ordered list of paths we have blazed
    if not here:  # no one here, done
        return frontier[0]
    while frontier:
        path = frontier.pop(0)
        here = path[-1][0]
        # check when pop off the path, every cheaper path is checked. so it's shortest path
        if not here:  ## That is, nobody left here
            return path
        for (state, action) in bsuccessors(path[-1]).items():
            if state not in explored:
                here, there, t = state
                explored.add(state)
                path2 = path + [action, state]
                # if not here:  ## no one here, done if check here (immediately) may not be shortest path
                #     return path2
                # else:
                frontier.append(path2)
                frontier.sort(key=elapsed_time)  ## best first search
    return []

def elapsed_time(path):
    return path[-1][2]

if __name__ == '__main__':
    def test():
        assert bsuccessors((frozenset([1, 'light']), frozenset([]), 3)) == {
                    (frozenset([]), frozenset([1, 'light']), 4): (1, 1, '->')}

        assert bsuccessors((frozenset([]), frozenset([2, 'light']), 0)) =={
                    (frozenset([2, 'light']), frozenset([]), 2): (2, 2, '<-')}

        assert bsuccessors((frozenset([1, 2, 3, 'light']), frozenset([]), 3)) == {
                    (frozenset([1, 3]), frozenset(['light', 2]), 5): (2, 2, '->'),
                    (frozenset([2]), frozenset([1, 3, 'light']), 6): (1, 3, '->'),
                    (frozenset([2, 3]), frozenset([1, 'light']), 4): (1, 1, '->'),
                    (frozenset([1]), frozenset(['light', 2, 3]), 6): (2, 3, '->'),
                    (frozenset([3]), frozenset([1, 2, 'light']), 5): (1, 2, '->'),
                    (frozenset([1, 2]), frozenset(['light', 3]), 6): (3, 3, '->')}

        assert bsuccessors((frozenset([1, 2, 5, 10, 'light']), frozenset([]), 3)) == {
                    (frozenset([2, 10]), frozenset([1, 5, 'light']), 8): (1, 5, '->'),
                    (frozenset([10, 5]), frozenset([1, 2, 'light']), 5): (1, 2, '->'),
                    (frozenset([1, 2, 5]), frozenset(['light', 10]), 13): (10, 10, '->'),
                    (frozenset([2, 5]), frozenset([1, 10, 'light']), 13): (1, 10, '->'),
                    (frozenset([1, 5]), frozenset(['light', 2, 10]), 13): (2, 10, '->'),
                    (frozenset([1, 2, 10]), frozenset(['light', 5]), 8): (5, 5, '->'),
                    (frozenset([1, 2]), frozenset(['light', 10, 5]), 13): (10, 5, '->'),
                    (frozenset([2, 10, 5]), frozenset([1, 'light']), 4): (1, 1, '->'),
                    (frozenset([1, 10, 5]), frozenset(['light', 2]), 5): (2, 2, '->'),
                    (frozenset([1, 10]), frozenset(['light', 2, 5]), 8): (2, 5, '->')}

        assert bridge_problem([1,2,5,10])[1::2] == \
                [(1, 2, '->'), (1, 1, '<-'), (10, 5, '->'), (2, 2, '<-'), (1, 2, '->')]
        return 'tests pass'

    import doctest
    class TestBridge: """
>>> path_cost(bridge_problem([1,2,5,10]))
17

## There are two equally good solutions
>>> S1 = [((2, 1, '->'), 2), ((1, 1, '<-'), 3), ((5, 10, '->'), 13), ((2, 2, '<-'), 15), ((2, 1, '->'), 17)]

>>> S2 = [((2, 1, '->'), 2), ((2, 2, '<-'), 4), ((5, 10, '->'), 14), ((1, 1, '<-'), 15), ((2, 1, '->'), 17)]
>>> path_actions(bridge_problem([1,2,5,10])) in (S1, S2)
True

## Try some other problems
>>> path_actions(bridge_problem([1,2,5,10,15,20]))
[((2, 1, '->'), 2), ((1, 1, '<-'), 3), ((5, 10, '->'), 13), ((2, 2, '<-'), 15), ((2, 1, '->'), 17), ((1, 1, '<-'), 18), ((15, 20, '->'), 38), ((2, 2, '<-'), 40), ((2, 1, '->'), 42)]

>>> path_actions(bridge_problem([1,2,4,8,16,32]))
[((2, 1, '->'), 2), ((1, 1, '<-'), 3), ((8, 4, '->'), 11), ((2, 2, '<-'), 13), ((1, 2, '->'), 15), ((1, 1, '<-'), 16), ((16, 32, '->'), 48), ((2, 2, '<-'), 50), ((2, 1, '->'), 52)]

>>> [path_cost(bridge_problem([1,2,4,8,16][:N])) for N in range(6)]
[0, 1, 2, 7, 15, 28]

>>> [path_cost(bridge_problem([1,1,2,3,5,8,13,21][:N])) for N in range(8)]
[0, 1, 1, 2, 6, 12, 19, 30]

# http://en.wikipedia.org/wiki/Bridge_and_torch_problem
>>> path_actions(bridge_problem([1,2,5,8]))
[((2, 1, '->'), 2), ((1, 1, '<-'), 3), ((5, 8, '->'), 11), ((2, 2, '<-'), 13), ((2, 1, '->'), 15)]

>>> path_cost(bridge_problem([1,2,5,8]))
15

>>> path_cost(bridge_problem([5,10,20,25]))
60
"""
    print test()
    print(doctest.testmod())
