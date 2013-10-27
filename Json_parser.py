#! /usr/bin/env python
# ---------------
# [JSON grammar](http://www.json.org/)
# use parser generator in `grammar_memo.py` to generator a JSON parser
from grammar_memo import grammar, parse
from verify import verify,check_left_recursion#,print_grammar

# in grammar description string :
# . ^ $ * + ? { } [ ] \ | ( ) should have a `\` behind them !!!!
# or Error may occur when performing regex matching

# NOTE: in udacity course solution, `members` and `elements` are used instead
# of `pairs` and `values` respectively
JSON = grammar( """
object => \{ \} | \{ pairs \}
pair => string : value
pairs =>  pair , pairs | pair
array  => \[ \] | \[ values \]
values  =>  value , values | value
value  => string | number | object | array | true | false | null
string => "[^"]*"
number => int frac exp | int frac | int exp | int
int => -?(?:0|[1-9][0-9]*)
frac => [.][0-9]+
exp => [eE][+-]?[0-9]+
""", whitespace='\s*')
# string => "(?:[^"\\]|\\(?:["\\/bfnrt]|[0-9a-f]{4}))*"

def json_parse(text):
    return parse('value', text, JSON)

if __name__ == '__main__':
    def test():
        verify(JSON)
        check_left_recursion(JSON)
        assert json_parse('"a"')         == (['value', ['string', '"a"']], '')
        assert json_parse('1')           == (['value', ['number', ['int', '1']]], '')
        assert json_parse('-1')          == (['value', ['number', ['int', '-1']]], '')
        assert json_parse('-123.456e+789') == (
            ['value', ['number', ['int', '-123'], ['frac', '.456'], ['exp', 'e+789']]], '')
        assert json_parse('[]')          == (['value', ['array', '[', ']']], '')
        assert json_parse('["testing"]') == (['value', ['array', '[', ['values', ['value', ['string', '"testing"']]], ']']], '')
        assert json_parse('[1]')         == (['value', ['array', '[', ['values', ['value', ['number', ['int', '1']]]], ']']], '')
        assert json_parse('[1,2]')       == (['value', ['array', '[', ['values', ['value', ['number', ['int', '1']]], ',', ['values', ['value', ['number', ['int', '2']]]]], ']']], '')
        assert json_parse('["testing", 1, 2, 3]') == (
                            ['value', ['array', '[', ['values', ['value',
                            ['string', '"testing"']], ',', ['values', ['value', ['number',
                            ['int', '1']]], ',', ['values', ['value', ['number',
                            ['int', '2']]], ',', ['values', ['value', ['number',
                            ['int', '3']]]]]]], ']']], '')
        assert json_parse('{}')          == (['value', ['object', '{', '}']], '')
        assert json_parse('{"age": 21, "state":"CO","occupation":"rides the rodeo"}') == (
                            ['value', ['object', '{', ['pairs', ['pair', ['string', '"age"'],
                            ':', ['value', ['number', ['int', '21']]]], ',', ['pairs',
                            ['pair', ['string', '"state"'], ':', ['value', ['string', '"CO"']]],
                            ',', ['pairs', ['pair', ['string', '"occupation"'], ':',
                            ['value', ['string', '"rides the rodeo"']]]]]], '}']], '')
        return 'tests pass'
    print test()
