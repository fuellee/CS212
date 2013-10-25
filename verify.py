#! /usr/bin/env python
def verify(G):
    lhs_tokens = set(G)-set(' ')
    rhs_tokens = set(token for alts in G.values() for alt in alts for token in alt if token.isalnum()) #can't handle '_'
    non_terms  = lhs_tokens
    terminals  = rhs_tokens-lhs_tokens
    orphans    = lhs_tokens-rhs_tokens  # Non-Terms that not in lhs

    def show(title,tokens):
        print title,'=',' '.join(sorted(tokens))
    show('Non-Terms', non_terms)  # G to lhs_tokens
    show('Terminals', terminals)  # should be regexes
    show('Suspects', [token for token in terminals if token.isalnum()])  # Terminals that looks like Non-Terms
    show('Orphans', orphans)

if __name__ == '__main__':
    from grammar import G
    verify(G)
