#! /usr/bin/env python
# -----------------
# User Instructions
#
# Write a function, subway, that takes lines as input (read more about
# the **lines notation in the instructor comments box below) and returns
# a dictionary of the form {station:{neighbor:line, ...}, ... }
#
# For example, when calling subway(boston), one of the entries in the
# resulting dictionary should be 'foresthills': {'backbay': 'orange'}.
# This means that foresthills only has one neighbor ('backbay') and
# that neighbor is on the orange line. Other stations have more neighbors:
# 'state', for example, has 4 neighbors.
#
# Once you've defined your subway function, you can define a ride and
# longest_ride function. ride(here, there, system) takes as input
# a starting station (here), a destination station (there), and a subway
# system and returns the shortest path.
#
# longest_ride(system) returns the longest possible ride in a given
# subway system.

# -------------
# Grading Notes
#
# The subway() function will not be tested directly, only ride() and
# longest_ride() will be explicitly tested. If your code passes the
# assert statements in test_ride(), it should be marked correct.

import collections
# subway :: {line:stations_str} -> {station:{neighbor:line,...},...}
def subway(**lines):
    """Define a subway map. Input is subway(linename='station1 station2...'...).
    Convert that and return a dict of the form: {station:{neighbor:line,...},...}"""
    ## your code here
    adj_graph = collections.defaultdict(dict)
    for line,stations in lines.items():
        stations = stations.split()
        for l,station,r in zip([None]+stations[:-1], stations, stations[1:]+[None]):
            if l is not None:
                adj_graph[station][l]=line
            if r is not None:
                adj_graph[station][r]=line
    return adj_graph

boston = subway(
    blue='bowdoin government state aquarium maverick airport suffolk revere wonderland',
    orange='oakgrove sullivan haymarket state downtown chinatown tufts backbay foresthills',
    green='lechmere science north haymarket government park copley kenmore newton riverside',
    red='alewife davis porter harvard central mit charles park downtown south umass mattapan')

# print boston
def ride(here, there, system=boston):
    "Return a path on the subway system from here to there."
    ## your code here
    # psuccessors :: state -> {state:action}
    # state :: station_name
    # action :: 'blue'|'orange'|'green'|'red'
    # path:: [state, action, state2, ...]
    is_goal = lambda state: state==there
    successors = lambda state: system[state]
    return shortest_path_search(here, successors, is_goal)


# def longest_ride(system):
#     """"Return the longest possible 'shortest path'
#     ride between any two stops in the system."""
#     ## your code here
#     successors = lambda state: system[state]
#     stations = system.keys()
#     longest_path = []
#     for i,here in enumerate(stations):
#         for there in stations[i+1:]:
#             ps=list(all_pathes(here, successors, lambda state: state==there))
#             if ps:
#                 p = ps[-1]
#                 if len(p)>len(longest_path):
#                     longest_path = p
#     return longest_path
def longest_ride(system):
    """"Return the longest possible 'shortest path'
    ride between any two stops in the system."""
    ## your code here
    successors = lambda state: system[state]
    stations = system.keys()
    longest_path = []
    for i,here in enumerate(stations):
        for there in stations[i+1:]:
            p=shortest_path_search(here, successors, lambda state: state==there)
            if len(p)>len(longest_path):
                longest_path = p
    return longest_path


def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []

def all_pathes(start, successors, is_goal):
    """Find all pathes from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        yield [start]
        return
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    yield path2
                else:
                    frontier.append(path2)



def path_states(path):
    "Return a list of states in this path."
    return path[0::2]

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

def test_ride():
    assert ride('mit', 'government') == [
        'mit', 'red', 'charles', 'red', 'park', 'green', 'government']
    assert ride('mattapan', 'foresthills') == [
        'mattapan', 'red', 'umass', 'red', 'south', 'red', 'downtown',
        'orange', 'chinatown', 'orange', 'tufts', 'orange', 'backbay', 'orange', 'foresthills']
    assert ride('newton', 'alewife') == [
        'newton', 'green', 'kenmore', 'green', 'copley', 'green', 'park', 'red', 'charles', 'red',
        'mit', 'red', 'central', 'red', 'harvard', 'red', 'porter', 'red', 'davis', 'red', 'alewife']
    assert (path_states(longest_ride(boston)) == [
        'wonderland', 'revere', 'suffolk', 'airport', 'maverick', 'aquarium', 'state', 'downtown', 'park',
        'charles', 'mit', 'central', 'harvard', 'porter', 'davis', 'alewife'] or
        path_states(longest_ride(boston)) == [
                'alewife', 'davis', 'porter', 'harvard', 'central', 'mit', 'charles',
                'park', 'downtown', 'state', 'aquarium', 'maverick', 'airport', 'suffolk', 'revere', 'wonderland'])
    assert len(path_states(longest_ride(boston))) == 16
    return 'test_ride passes'

print test_ride()
