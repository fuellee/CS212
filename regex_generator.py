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
def opt(x):     return alt(epsilon, x)
# seq returns a function (delay the computation)
# genseq do the computation immediately
def seq(x,y):   return lambda Ns: genseq(x, y, Ns)
# for plus(opt(lit('a'))), can cause a dead loop with out arg `startx` (left recurrsion)
def plus(x):    return lambda Ns: genseq(x, star(x), Ns, startx=1)  #Tricky
def star(x):    return lambda Ns: opt(plus(x))(Ns)  # x* : (x+)?
# oneof is slightly different, it take a string as arg
# returns set of single chars in that string if 1 in Ns
def oneof(chars):return lambda Ns: set(chars) if 1 in Ns else null

dot = oneof('?')   # not expand `dot` to 256 chars, cause it expands too much. use a `?` stand for `dot`
epsilon = lit('')  # pattern matches empty string

#  like seq(x,y), but compute result immediately
def genseq(x, y, Ns, startx=0):
    """Set of matches to xy whose total len is in Ns, with x-match's len in Ns and
    >= startx"""
    # Tricky part: x+ is defined as: x+ = x x* To stop the recursion, the first x
    # must generate at least 1 char, and then the recursive x* has that many fewer
    # characters. We use startx = 1 to say that x must match at least 1 character
    if not Ns:
        return null
    else:
        x_matches = x(set(range(startx, max(Ns)+1)))  # x consume at least `startx` chars, resolve left recurrsion
        x_matches_lens = set(map(len ,x_matches))
        y_matches_lens = set(n-x_l for x_l in x_matches_lens for n in Ns if n-x_l>=0)
        y_matches = y(y_matches_lens)
        return set(str_x+str_y
                   for str_x in x_matches
                   for str_y in y_matches
                   if len(str_x)+len(str_y) in Ns)

def test_simple_generator():
    f = lit('hello')
    assert f(set([1, 2, 3, 4, 5])) == set(['hello'])
    assert f(set([1, 2, 3, 4]))    == null
    assert lit('hello')(set([4])) == set()
    assert lit('hello')(set([6])) == set()

    g = alt(lit('hi'), lit('bye'))
    assert g(set([1, 2, 3, 4, 5, 6])) == set(['bye', 'hi'])
    assert g(set([1, 3, 5])) == set(['bye'])

    h = oneof('theseletters')
    assert h(set([1, 2, 3])) == set(['t', 'h', 'e', 's', 'l', 'r'])
    assert h(set([2, 3, 4])) == null
    return 'test_simple_generator pass'

def test_seqgen():
    def N(hi):
        return set(range(hi+1))
    a, b, c = map(lit, 'abc')
    assert (genseq(oneof('bcfhrsm'), lit('at'), set(range(3+1))) ==
            set(['bat', 'cat', 'fat', 'hat', 'mat', 'rat', 'sat']))
    assert (seq(oneof('bcfhrsm'), lit('at'))(N(3)) ==
            set(['bat', 'cat', 'fat', 'hat', 'mat', 'rat', 'sat']))
    assert star(oneof('ab'))(N(2)) == set(['', 'a', 'aa', 'ab', 'ba', 'bb', 'b'])
    assert (seq(star(a), seq(star(b), star(c)))(set([4])) ==
            set(['aaaa', 'aaab', 'aaac', 'aabb', 'aabc', 'aacc', 'abbb',
                 'abbc', 'abcc', 'accc', 'bbbb', 'bbbc', 'bbcc', 'bccc', 'cccc']))
    assert (seq(plus(a), seq(plus(b), plus(c)))(set([5])) ==
            set(['aaabc', 'aabbc', 'aabcc', 'abbbc', 'abbcc', 'abccc']))
    assert (seq(star(alt(a, b)), opt(c))(set([3])) ==
            set(['aaa', 'aab', 'aac', 'aba', 'abb', 'abc', 'baa',
                 'bab', 'bac', 'bba', 'bbb', 'bbc']))
    return 'test_seqgen passes'

if __name__ == '__main__':
    print(test_simple_generator())
    print(test_seqgen())
