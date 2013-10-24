def split(text, sep=None, maxsplit=-1):
    "like str.split applied to text, but **strips whitespace** from each piece"
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]

def grammar(description):
    """convert a description to grammar"""
    G={}
    for line in split(description,"\n"):
        lhs, rhs = split(line,"=>")
        G[lhs]=tuple(map(split, split(rhs, ' | ')))
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

assert (grammar(G_description)) ==\
        {'Term': (['Factor', '[*/]', 'Term'], ['Factor']),
         'Exps': (['Exp', '[,]', 'Exps'], ['Exp']),
         'Funcall': (['Var', '[(]', 'Exps', '[)]'],),
         'Num': (['[-+]?[0-9]+([.][0-9]*)?'],),
         'Exp': (['Term', '[+-]', 'Exp'], ['Term']),
         'Factor': (['Funcall'], ['Var'], ['Num'], ['[(]', 'Exp', '[)]']),
         'Var': (['[a-zA-Z_]\\w*'],)}
