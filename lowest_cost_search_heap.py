#! /usr/bin/env python
# -----------------
# User Instructions
#
# In this problem, you will generalize the bridge problem
# by writing a function bridge_problem3, that makes a call
# to lowest_cost_search.

import heapq
def lowest_cost_search(start, successors, is_goal, action_cost):
    """Return the lowest cost path, starting from start state,
    and considering successors(state) => {state:action,...},
    that ends in a state for which is_goal(state) is true,
    where the cost of a path is the sum of action costs,
    which are given by action_cost(action)."""
    # frontier is a heap
    # frontier :: [(path_cost, path)]
    # path :: [state, (action, total_cost), state ...]  # start and end with state
    Fail = []
    def final_state(path): return path[-1]

    explored = set() # set of states we have visited
    frontier = []
    heapq.heappush(frontier, (0,[start])) # init heap, cost of start is 0
    while frontier:
        pcost,path = heapq.heappop(frontier)
        state1 = final_state(path)
        if is_goal(state1):

            # print pcost

            return path
        explored.add(state1)
        for (state, action) in successors(state1).items():
            if state not in explored:
                total_cost = pcost + action_cost(action)
                path2 = path + [action, state]
                heapq.heappush(frontier, (total_cost, path2))
    return Fail

def actions(path): return path[1::2]  # actually returns [(actions,path_cost)...]
def states(path): return path[::2]

if __name__ == '__main__':
    def bridge_problem3(here):
        """Find the fastest (least elapsed time) path to
        the goal in the bridge problem."""
        start = (frozenset(here)|{'light'},frozenset())
        successors = bsuccessors2
        def all_over(state):
            here, there = state
            return not here or here == set(['light'])
        action_cost = bcost
        return lowest_cost_search(start, successors, all_over, action_cost)

    def bsuccessors2(state):
        """Return a dict of {state:action} pairs.  A state is a (here, there) tuple,
        where here and there are frozensets of people (indicated by their times) and/or
        the light."""
        here, there = state
        if 'light' in here:
            return dict(((here  - frozenset([a, b, 'light']),
                        there | frozenset([a, b, 'light'])),
                        (a, b, '->'))
                        for a in here if a is not 'light'
                        for b in here if b is not 'light')
        else:
            return dict(((here  | frozenset([a, b, 'light']),
                        there - frozenset([a, b, 'light'])),
                        (a, b, '<-'))
                        for a in there if a is not 'light'
                        for b in there if b is not 'light')

    def bcost(action):
        "Returns the cost (a number) of an action in the bridge problem."
        # An action is an (a, b, arrow) tuple; a and b are times; arrow is a string
        a, b, arrow = action
        return max(a, b)

    def test():
        here = [1, 2, 5, 10]
        print actions(bridge_problem3(here))
        # assert actions(bridge_problem3(here)) == [((2, 1, '->'), 2),
        #                                           ((2, 2, '<-'), 4),
        #                                           ((5, 10, '->'), 14),
        #                                           ((1, 1, '<-'), 15),
        #                                           ((2, 1, '->'), 17),]
        # assert bridge_problem3(here) == [
        #         (frozenset([1, 2, 'light', 10, 5]), frozenset([])),
        #         ((2, 1, '->'), 2),
        #         (frozenset([10, 5]), frozenset([1, 2, 'light'])),
        #         ((2, 2, '<-'), 4),
        #         (frozenset(['light', 10, 2, 5]), frozenset([1])),
        #         ((5, 10, '->'), 14),
        #         (frozenset([2]), frozenset([1, 10, 5, 'light'])),
        #         ((1, 1, '<-'), 15),
        #         (frozenset([1, 2, 'light']), frozenset([10, 5])),
        #         ((2, 1, '->'), 17),
        #         (frozenset([]), frozenset([1, 10, 2, 5, 'light']))]
        return 'test passes'

    print test()
