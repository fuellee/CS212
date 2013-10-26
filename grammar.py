#! /usr/bin/env python

import re
from trace_tool import trace,disabled

def split(text, sep=None, maxsplit=-1):
    "like str.split applied to text, but **strips whitespace** from each piece"
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]

def grammar(description, whitespace=r'\s*'):
    """Convert a description to grammar. Each line is a rule for a
    non-terminal symbol; it looks like this:
        Symbol => A1 A1 .. | B1 B2 ... | C1 C2 ...
    where the right-hand side is one or more `alternatives`, separated by
    the '|' sign. Each `alternative` is a sequence of `atoms`, separated by
    spaces. An `atom` is either a `symbol` on some left-hand side, or it is
    a regular expression that will be passed to re.match to match a token.
    Notation for *, +, or ? not allowed in a rule alternative (but ok within a token).
    Use '\' to continue long lines. You must include spaces or tabs around '=>' and '|'.
    That's within the grammar description itself.
    The grammar that gets defined allows whitespace between tokens by default specify ' '
    as the second argument to `grammar()` to disallow this (or supply any regex to describe
    allowable whitespace between tokens)"""
    G={' ':whitespace}
    description = description.replace('\t',' ')  # handle tabs in description
    for line in split(description,"\n"):
        lhs, rhs = split(line,"=>")
        alternatives = split(rhs, ' | ')
        G[lhs]=tuple(map(split, alternatives))
    return G

G_description = r"""
Exp => Term [+-] Exp | Term
Term => Factor [*/] Term | Factor
Factor => Funcall | Var | Num | [(] Exp [)]
Funcall => Var [(] Exps [)]
Exps => Exp [,] Exps | Exp
Var => [a-zA-Z_]\w*
Num => [-+]?[0-9]+([.][0-9]*)?
"""
G = grammar(G_description)
if __name__ == '__main__':
    assert (grammar(G_description)) ==\
            {' ': '\\s*',
            'Term': (['Factor', '[*/]', 'Term'], ['Factor']),
            'Exps': (['Exp', '[,]', 'Exps'], ['Exp']),
            'Funcall': (['Var', '[(]', 'Exps', '[)]'],),
            'Num': (['[-+]?[0-9]+([.][0-9]*)?'],),
            'Exp': (['Term', '[+-]', 'Exp'], ['Term']),
            'Factor': (['Funcall'], ['Var'], ['Num'], ['[(]', 'Exp', '[)]']),
            'Var': (['[a-zA-Z_]\\w*'],)}


# parse(symbol, text, G) -> (parsed_tree, remander)
# remander is a single string (not a set since grammar should be unambiguous)
# convention: Fail = (None,None)
# can parse:
# category     | e.g.            | handler(subroutine)
# -------------------------------------------------------
# atomic_expr  | 'Exp'           | parse_atom
# regex        | '[+-]'          | tokenizer, (re.match)
# alternatives | ([...], [...])  | parse_atom
# list_atoms   | [..., ..., ...] | parse_atoms

Fail = (None, None)
if __name__ != '__main__':
    trace = disabled  # disable `trace`, no trace print
def parse(start_symbol, text, grammar):
    """Example call: parse('Exp', '3*x + b', G)
    Retrun a (parsed_tree, remainder) pair. If remainder is '', parsing is done
    Failure iff remainder is `None`. This is a deterministic PEG parser,
    so rule order (left-to-right) matters. Do 'E => T op E | T' , putting the
    **longest parse first**; **don't** do 'E => T | T op E'
    Alse, no left recursion allowed: don't do 'E => E op T'

    See: http://en.wikipedia.org/wiki/Parsing_expression_grammar
    """
    # tokenizer pattern means: atom with optional blanks before it
    tokenizer = grammar[' '] + '(%s)'
    # (%s) for atom replacement. enclosed within parentheses means a `group`
    @trace
    def parse_atoms(atoms, remainder):
        result = []
        for atom in atoms:
            tree, remainder = parse_atom(atom, remainder)
            if remainder is None:
                return Fail
            result.append(tree)
        return (result, remainder)

    @trace
    def parse_atom(atom, remainder):
        # atom is a **Non-Terminal**, try match `alternatives`
        if atom in grammar:
            for alternative in grammar[atom]:
                tree, rem = parse_atoms(alternative, remainder)  # `rem` and `remainder` are different!
                if rem is not None:  # return after first successful match
                    return ([atom]+tree, rem)
            return Fail  # no matching rule (alternatives)
        # atom is a **Terminal**, described by regex. match chars start of text
        else:
            terminal_with_blank = re.match(tokenizer%atom, remainder)
            if not terminal_with_blank:  # can't match this terminal
                return Fail
            else:
                return (terminal_with_blank.group(1), remainder[terminal_with_blank.end():])
                #`m.group(1)` take the terminal(without blanks)

    return parse_atom(start_symbol, text)

if __name__ == '__main__':
    assert parse('Exp', 'a * x', G) ==\
            (['Exp', ['Term', ['Factor', ['Var', 'a']],         # parsed_tree
                    '*',
                    ['Term', ['Factor', ['Var', 'x']]]]],
            '')                                                # remander
