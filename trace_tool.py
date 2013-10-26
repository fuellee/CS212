# ---------------
# User Instructions
#
# Modify the function, trace, so that when it is used
# as a decorator it gives a trace as shown in the previous
# video. You can test your function by applying the decorator
# to the provided fibonnaci function.
#
# Note: Running this in the browser's IDE will not display
# the indentations.

from functools import update_wrapper


def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

callcounts = {}
@decorator
def countcalls(f):
    "Decorator that makes the function count calls to it, in callcounts[f]."
    def _f(*args):
        callcounts[_f] += 1
        return f(*args)
    callcounts[_f] = 0
    return _f

@decorator
def trace(f):
    indent = '    '  # 4 blank
    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print '%s--> %s' % (trace.level*indent, signature)
        trace.level += 1  # increase level everytime `f` is called
        try:
            result = f(*args)  # decrease level evertime `f` returns (computed)
            # if f(*args) throws a error,just throw it out, and go back level normally
            # printed stack won't be massed by errors
            print '%s<-- %s == %s' % ((trace.level-1)*indent,
                                      signature, result)
        finally:
            trace.level -= 1
        return result
    trace.level = 0
    return _f

@decorator
def disabled(f):
    """ a decorator do no thing
    e.g: `trace = disabled` to turn off trace decorator
    """
    return f

# trace = disabled  # decorator `trace` is `I` now (do no thing)
@trace
def fib(n):
    if n == 0 or n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
# apply decorators to lambda expr:
# fib = trace(lambda n:1 if n<=1 else fib(n-1)+fib(n-2))

if __name__ == '__main__':
    fib(6)
