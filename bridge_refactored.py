#! /usr/bin/env python
# -----------------
# User Instructions
#
# write a function, bsuccessors2 that takes a state as input
# and returns a dictionary of {state:action} pairs.
#
# The new representation for a path should be a list of
# [state, (action, total time), state, ... , ], though this
# function will just return {state:action} pairs and will
# ignore total time.
#
# The previous bsuccessors function is included for your reference.

import itertools
# state :: (here, there)
# here  :: frozenset
# there :: frozenset
# bsuccessors :: state -> {state:action}
def bsuccessors(state):
    """Return a dict of {state:action} pairs. A state is a
    (here, there) tuple, where here and there are frozensets
    of people (indicated by their travel times) and/or the light."""
    # your code here
    here, there = state
    successors = {}
    (from_, to, arrow) = (here,there,'->') if 'light' in here else (there,here,'<-')

    for (person2,person1) in itertools.combinations_with_replacement(from_-{'light'} ,2):
        team = {person1, person2, 'light'}
        state = (from_^team, to^team) if arrow is '->' else (to^team, from_^team)
        action = (person1, person2, arrow)
        successors[state]=action
    return successors

# path :: [state, (action, total_cost), state, ... ]
# path_cost :: path -> cost
def path_cost(path):
    """The total cost of a path (which is stored in a tuple
    with the final action."""
    if len(path) < 3:
        return 0
    else:
        action, total_cost = path[-2]
        return total_cost

# bcost :: action -> int
def bcost(action):
    """Returns the cost (a number) of an action in the
    bridge problem."""
    # An action is an (a, b, arrow) tuple; a and b are
    # times; arrow is a string.
    a, b, arrow = action
    return max(a,b)

# frontier :: [path]
# best first search
def bridge_problem(here):
    here = frozenset(here) | {'light'}
    explored = set()
    frontier = [ [(here, frozenset())]]  # ordered list of paths we have blazed
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
                here, there = state
                explored.add(state)
                path2 = path + [(action, bcost(action)), state]
                # if not here:  ## no one here, done if check here (immediately) may not be shortest path
                #     return path2
                # else:
                frontier.append(path2)
                frontier.sort(key=path_cost)  ## best first search
    return []

# path_actions :: path -> [action]
def path_actions(path):
    return map(lambda action_cost:action_cost[0], path[1::2])

if __name__ == '__main__':
    def test():
        # path_cost
        assert path_cost(('fake_state1', ((2, 5, '->'), 5), 'fake_state2')) == 5
        assert path_cost(('fs1', ((2, 1, '->'), 2), 'fs2', ((3, 4, '<-'), 6), 'fs3')) == 6
        # bcost
        assert bcost((4, 2, '->'),) == 4
        assert bcost((3, 10, '<-'),) == 10
        # bsuccesssor
        here1 = frozenset([1, 'light'])
        there1 = frozenset([])

        here2 = frozenset([1, 2, 'light'])
        there2 = frozenset([3])

        assert bsuccessors((here1, there1)) == {
                (frozenset([]), frozenset([1, 'light'])): (1, 1, '->')}
        assert bsuccessors((here2, there2)) == {
                (frozenset([1]), frozenset(['light', 2, 3])): (2, 2, '->'),
                (frozenset([2]), frozenset([1, 3, 'light'])): (1, 1, '->'),
                (frozenset([]), frozenset([1, 2, 3, 'light'])): (2, 1, '->')}

        print path_actions(bridge_problem([1,2,5,10]))
        assert path_actions(bridge_problem([1,2,5,10])) == \
                [(1, 2, '->'), (1, 1, '<-'), (10, 5, '->'), (2, 2, '<-'), (1, 2, '->')]
        return 'tests pass'

#     import doctest
#     class TestBridge: """
# >>> path_cost(bridge_problem([1,2,5,10]))
# 17
#
# ## There are two equally good solutions
# >>> S1 = [((2, 1, '->'), 2), ((1, 1, '<-'), 3), ((5, 10, '->'), 13), ((2, 2, '<-'), 15), ((2, 1, '->'), 17)]
#
# >>> S2 = [((2, 1, '->'), 2), ((2, 2, '<-'), 4), ((5, 10, '->'), 14), ((1, 1, '<-'), 15), ((2, 1, '->'), 17)]
# >>> path_actions(bridge_problem([1,2,5,10])) in (S1, S2)
# True
#
# ## Try some other problems
# >>> path_actions(bridge_problem([1,2,5,10,15,20]))
# [((2, 1, '->'), 2), ((1, 1, '<-'), 3), ((5, 10, '->'), 13), ((2, 2, '<-'), 15), ((2, 1, '->'), 17), ((1, 1, '<-'), 18), ((15, 20, '->'), 38), ((2, 2, '<-'), 40), ((2, 1, '->'), 42)]
#
# >>> path_actions(bridge_problem([1,2,4,8,16,32]))
# [((2, 1, '->'), 2), ((1, 1, '<-'), 3), ((8, 4, '->'), 11), ((2, 2, '<-'), 13), ((1, 2, '->'), 15), ((1, 1, '<-'), 16), ((16, 32, '->'), 48), ((2, 2, '<-'), 50), ((2, 1, '->'), 52)]
#
# >>> [path_cost(bridge_problem([1,2,4,8,16][:N])) for N in range(6)]
# [0, 1, 2, 7, 15, 28]
#
# >>> [path_cost(bridge_problem([1,1,2,3,5,8,13,21][:N])) for N in range(8)]
# [0, 1, 1, 2, 6, 12, 19, 30]
#
# # http://en.wikipedia.org/wiki/Bridge_and_torch_problem
# >>> path_actions(bridge_problem([1,2,5,8]))
# [((2, 1, '->'), 2), ((1, 1, '<-'), 3), ((5, 8, '->'), 11), ((2, 2, '<-'), 13), ((2, 1, '->'), 15)]
#
# >>> path_cost(bridge_problem([1,2,5,8]))
# 15
#
# >>> path_cost(bridge_problem([5,10,20,25]))
# 60
# """
    print test()
    # print(doctest.testmod())
