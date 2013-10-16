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
  simple profile tool for function calls
* `solving_cryptarithmetic.py`
  - example for using `eval`
  - profile (python -m cPython solving_cryptarithmetic.py) shows `eval` consumes a large percentage of time. `eval` parses formulae in every call, compile that into functions is a better approach
* `fast_solver.py`
  - optimized version of `solving_cryptarithmetic.py`
  - use `eval` to compile frequently computed formulas to functions in python
  - when assembling strings to a legal function to feed `eval`, I feel missing Scheme. S-expr rocks!
