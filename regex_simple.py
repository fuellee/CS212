#! /usr/bin/env python
## Rob Pike's essay: http://tinyurl.com/pike-regexp

def match(pattern, text):
    """ Return True if pattern appears at the start of text """
    if pattern == '':
        return True
    elif pattern == '$':
        return (text == '')
    elif len(pattern) > 1 and pattern[1] in '*?':
        p, op, pat = pattern[0], pattern[1], pattern[2:]
        if op == '*':
            return match_star(p, pat, text)
        elif op == '?':
            if match1(p, text) and match(pat, text[1:]):
                return True
            else:
                return match(pat, text)
    else:
        return (match1(pattern[0], text) and
                match( pattern[1:],text[1:])) # fill in this line

def match1(p,text):
    """Return true if first character of text matches
    pattern character p"""
    if not text:
        return False
    # elif p=='.':
    #     return True
    # else:
    #     return p==text[0]
    return p=='.' or p==text[0]

def match_star(p,pattern,text):
    """Return true if any number of char p,
    followed by pattern, matches text."""
    # match r"p*"
    return (match(pattern,text) or  # o p (no p)
            (match1(p,text) and match_star(p,pattern,text[1:]))) # 1 or more p

def test():
    # test cases for $
    assert match('$','') == True
    assert match('$','a') == False
    assert match('b$','a') == False
    assert match('a$','a') == True
    # test cases for ?
    assert match ('a?','') == True
    assert match('aa?','a') == True
    assert match('aa?','aa') == True
    assert match('aa?$','aaa') == False  # pattern does not appear at he start of
    # test cases for *
    assert match('a*','aaabb') == True
    assert match('a*$','aaa') == True
    assert match('aa*$','c') == False
    assert match('a*$','c') == False
    # test cases for .
    assert match('.', '') == False
    assert match('.', 'c') == True
    assert match('.*', 'casdfasdfasd') == True
    print "test pass"


if __name__ == '__main__':
    test()
