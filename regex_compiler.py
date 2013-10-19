#! /usr/bin/env python
#---------------
# User Instructions
#
# Fill out the API by completing the entries for alt,
# star, plus, and eol.
from __future__ import print_function

null = frozenset()

def lit(s): return lambda text: {text[len(s):]} if text.startswith(s) else null
def seq(x, y): return lambda text: set().union(*map(y, x(text)))
# def alt(x, y): return lambda text: set().union(x(text),y(text))
def alt(x, y): return lambda text: x(text) | y(text)  # '|' means set union
def oneof(chars): return lambda text: {text[1:]} if text[0] in chars else null
dot = lambda text: {text[1:]} if text is not '' else null
eol = lambda text: {''} if text is '' else null

def star(x): return lambda text: ({text}| set(t2 for t1 in x(text) if t1!=text for t2 in star(x)(t1)))
def plus(x):return seq(x, star(x))
def opt(x): return alt(lit(''), x) #opt(x) means that x is optional

def test_compiled_recognizer():
    g = alt(lit('a'), lit('b'))
    assert g('abc') == set(['bc'])
    g = seq(lit('a'), lit('b'))
    assert g('abc') == {'c'}
    return 'compiled recognizer tests pass'

# print test_compiled_recognizer()

#---------------
# User Instructions
#
# Complete the search and match functions. Match should
# match a pattern only at the start of the text. Search
# should match anywhere in the text.
def match(pattern, text):
    "Match pattern against start of text; return longest match found or None."
    remainders = pattern(text)
    if remainders:
        shortest = min(remainders, key=len)
        return text[:len(text)-len(shortest)]

def search(pattern, text):
    "Match pattern anywhere in text; return longest earliest match or None."
    for i in range(len(text) or 1):  # special case: text is '' then len(text)==0, should match at least once
        m = match(pattern, text[i:])
        if m is not None:
            return m

def test_search_match():
    assert match(star(lit('a')),'aaabcd') == 'aaa'
    assert match(alt(lit('b'), lit('c')), 'ab') == None
    assert match(alt(lit('b'), lit('a')), 'ab') == 'a'
    assert match(lit('hello'), 'hello how are you?') == 'hello'
    assert match(lit('x'), 'hello how are you?') == None
    assert match(oneof('xyz'), 'x**2 + y**2 = r**2') == 'x'
    assert match(oneof('xyz'), '   x is here!') == None

    assert match(star(lit('a')), 'aaabcd') == 'aaa'
    assert match(lit('abc'), 'abc') == 'abc'
    assert match(alt(lit('b'), lit('c')), 'ab') == None
    assert match(alt(lit('b'), lit('a')), 'ab') == 'a'
    assert search(lit(''), '') == ''
    assert search(alt(lit('b'), lit('c')), 'ab') == 'b'
    assert search(star(alt(lit('a'), lit('b'))), 'ab') == 'ab'
    assert search(alt(lit('b'), lit('c')), 'ad') == None
    assert lit('abc')('abcdef') == set(['def'])
    assert (seq(lit('hi '), lit('there '))('hi there nice to meet you')
            == set(['nice to meet you']))
    assert match(seq(star(lit('a')),star(lit('b'))),'aaaaaaabbbbbc')=='aaaaaaabbbbb'
    assert alt(lit('dog'), lit('cat'))('dog and cat') == set([' and cat'])
    assert dot('am i missing something?') == set(['m i missing something?'])
    assert dot('') == frozenset([])
    assert oneof('a')('aabc123') == set(['abc123'])
    assert oneof('abc')('babc123') == set(['abc123'])
    assert oneof('abc')('dabc123') == frozenset([])
    assert eol('') == set([''])
    assert eol('not end of line') == frozenset([])
    assert star(lit('hey'))('heyhey!') == set(['!', 'heyhey!', 'hey!'])
    assert plus(lit('hey'))('heyhey!') == set(['!', 'hey!'])
    assert opt(lit('hey'))('heyhey!') == set(['hey!', 'heyhey!'])

    return 'match-search tests pass'

print(test_search_match())

