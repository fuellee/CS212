#! /usr/bin/env python

# pat({int}) -> {str}
# e.g:
# pat = lit('hello')
# pat({1,2,3,4,5}) == {'hello'}

null = frozenset([])
# Ns:: {int}
def lit(s):
    set_s = {s}  # pull set(s) out, precompute it
    return lambda Ns: set_s if len(s) in Ns else null
def alt(x,y):   return lambda Ns: x(Ns)|y(Ns)
def opt(x):     return lambda Ns: alt(epsilon, x)
# seq returns a function (delay the computation)
# genseq do the computation immediately
def seq(x,y):   return lambda Ns: genseq(x, y, Ns)
def plus(x):    return lambda Ns: genseq(x, star(x), Ns, startx=1)  #Tricky
def star(x):    return lambda Ns: (opt(plus(x)))(Ns)  # x* : (x+)?
# oneof is slightly different, it take a string as arg
# returns set of single chars in that string if 1 in Ns
def oneof(chars):return lambda Ns: set(chars) if 1 in Ns else null

dot = oneof('?')   # not expand `dot` to 256 chars, cause it expands too much. use a `?` stand for `dot`
epsilon = lit('')  # pattern matches empty string

def genseq(x, y, Ns, startx=0):
    """Set of matches to xy whose total len is in Ns, with x-match's len in Ns and
    >= startx"""
    pass

def test():
    f = lit('hello')
    assert f(set([1, 2, 3, 4, 5])) == set(['hello'])
    assert f(set([1, 2, 3, 4]))    == null

    g = alt(lit('hi'), lit('bye'))
    assert g(set([1, 2, 3, 4, 5, 6])) == set(['bye', 'hi'])
    assert g(set([1, 3, 5])) == set(['bye'])

    h = oneof('theseletters')
    assert h(set([1, 2, 3])) == set(['t', 'h', 'e', 's', 'l', 'r'])
    assert h(set([2, 3, 4])) == null
    return 'tests pass'

print(test())
