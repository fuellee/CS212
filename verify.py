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
    from grammar import G,grammar,parse
    verify(G)
    print "------------------"
    ## Parsing URLs
    ## See http://www.w3.org/Addressing/URL/5_BNF.html

    URL = grammar("""
    url => httpaddress | ftpaddress | mailtoaddress
    httpaddress => http:// hostport /path? ?search?
    ftpaddress => ftp:// login / path ; ftptype | ftp:// login / path
    /path? => / path | ()
    ?search? => [?] search | ()
    mailtoaddress => mailto: xalphas @ hostname
    hostport => host : port | host
    host => hostname | hostnumber
    hostname => ialpha . hostname | ialpha
    hostnumber => digits . digits . digits . digits
    ftptype => A formcode | E formcode | I | L digits
    formcode => [NTC]
    port => digits | path
    path => void | segment / path | segment
    segment => xalphas
    search => xalphas + search | xalphas
    login => userpassword hostport | hostport
    userpassword => user : password @ | user @
    user => alphanum2 user | alphanum2
    password => alphanum2 password | password
    path => void | segment / path | segment
    void => ()
    digits => digit digits | digit
    digit => [0-9]
    alpha => [a-zA-Z]
    safe => [-$_@.&+]
    extra => [()!*''""]
    escape => % hex hex
    hex => [0-9a-fA-F]
    alphanum => alpha | digit
    alphanums => alphanum alphanums | alphanum
    alphanum2 => alpha | digit | [-_.+]
    ialpha => alpha xalphas | alpha
    xalphas => xalpha xalphas | xalpha
    xalpha => alpha | digit | safe | extra | escape
    """, whitespace = '()')
    print "--URL grammar:\n",(URL)
    print
    verify(URL)
    print
    print "--parsed http://www.w3.org/Addressing/URL/5_BNF.html:\n",(parse('url', 'http://www.w3.org/Addressing/URL/5_BNF.html', URL))


