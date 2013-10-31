#! /usr/bin/env python
# -----------------
# User Instructions
#
# In this problem, you will solve the pouring problem for an arbitrary
# number of glasses. Write a function, more_pour_problem, that takes
# as input capacities, goal, and (optionally) start. This function should
# return a path of states and actions.
#
# Capacities is a tuple of numbers, where each number represents the
# volume of a glass.
#
# Goal is the desired volume and start is a tuple of the starting levels
# in each glass. Start defaults to None (all glasses empty).
#
# The returned path should look like [state, action, state, action, ... ]
# where state is a tuple of volumes and action is one of ('fill', i),
# ('empty', i), ('pour', i, j) where i and j are indices indicating the
# glass number.
from shortest_path_search import shortest_path_search

def more_pour_problem(capacities, goal, start=None):
    """The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number."""
    # your code here
    def is_goal(state): return goal in state
    # psuccessors :: state -> {state:action}
    # path:: [state, action, state2, ...]
    # action :: ('fill', i) | ('empty', i) | ('pour', i, j)
    def psuccessors(state):
        ss = {}
        for (i,s_i) in enumerate(state):
            if s_i!=0:
                ss[replace(state,i,0)]=('empty',i)
                for (j,s_j) in enumerate(state):
                    if i!=j:
                        exchange = min(s_i,capacities[j]-s_j)
                        tmp_state = list(state)
                        (tmp_state[i],tmp_state[j]) = (s_i-exchange, s_j+exchange)
                        ss[tuple(tmp_state)]=('pour',i,j)
            if s_i!=capacities[i]:
                ss[replace(state,i,capacities[i])]=('fill', i)
        return ss

    def replace(seq,index,val):
        result = list(seq)
        result[index]=val
        return type(seq)(result)

    if start==None: start = tuple(0 for _ in capacities)
    return shortest_path_search(start, psuccessors, is_goal)

if __name__ == '__main__':
    def test_more_pour():
        assert more_pour_problem((1, 2, 4, 8), 4) == [
            (0, 0, 0, 0), ('fill', 2), (0, 0, 4, 0)]
        assert more_pour_problem((1, 2, 4), 3) == [
            (0, 0, 0), ('fill', 2), (0, 0, 4), ('pour', 2, 0), (1, 0, 3)]
        starbucks = (8, 12, 16, 20, 24)
        assert not any(more_pour_problem(starbucks, odd) for odd in (3, 5, 7, 9))
        assert all(more_pour_problem((1, 3, 9, 27), n) for n in range(28))
        assert more_pour_problem((1, 3, 9, 27), 28) == []
        return 'test_more_pour passes'

    print test_more_pour()
