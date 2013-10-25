Udacity CS212 Design of Computer Programs
=========================================

Code for Udacity CS212 Design of Computer Programs

Unit 1
------
* `poker.py`
* `poker_refactored.py`  
  one to one correspondence between hand of cards and interger paritition
* `shuffle.py`   
  need explaination form probabilistic perspective

* `seven_card_stud.py`  
  choose the best hand(5 cards) from more than 5 cards
* `jokers_wild.py`  
  `itertools.produce` to build the whole problem space  
  [constant] * [wildcard possiblilities ..] ...

Unit 2
------
* `time_calls.py`
  simple profile tool for function calls;  
  `zebra_puzzle` inside
* `solving_cryptarithmetic.py`
  - example for using `eval`
  - profile (python -m cPython solving_cryptarithmetic.py) shows `eval` consumes a large percentage of time. `eval` parses formulae in every call, compile that into functions is a better approach
* `fast_solver.py`
  - optimized version of `solving_cryptarithmetic.py`
  - use `eval` to compile frequently computed formulas to functions in python
  - when assembling strings to a legal function to feed `eval`, I feel missing Scheme. S-expr rocks!

* `floor_puzzie.py`
* `subpalindrome.py`

Unit 3
------
* `regex_simple.py`  
  a simple regex interpreter, patterns have no structure, no grouping.
* `regex_interpreter.py`  
  a regex interpreter, regex patterns have inner structure.
* `regex_compiler.py`  
  a regex compiler, compile regex patterns(looks like function calls) to python functions.


* `regex_generator.py`  
  a regex generator, generate instances of a regex pattern of some certain length

* `memoization.py`
  - `n_ary`: decorator that makes a binary function n ary.
  - `memo` : decorator that caches the return value for each call to f(args). look `cache[args]` up before actually call the function.
* `trace_tool.py`
  - `trace`:trace function call stack inplemented with a **decorator**, pretty print the result with indentation(`trace.level`)
  - `countcalls`: decorator that makes the function count calls to it, store in `callcount[f]`

* `grammar.py`  
  a simple top-down deterministic PEG parser 
* `grammar_memo.py`  
  - almost the same as `grammar.py`, the only difference is subroutine `parse_atom` is memoized(with @memo defined in `memoization.py`)
  - reduce function calls (`parse_atom` and `parse_atoms`) from **180** to **66**
