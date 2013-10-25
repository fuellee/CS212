#! /usr/bin/env python
import functools  # functools.update_wrapper for `decorator`
def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return functools.update_wrapper(d(fn), fn)
    return _d
decorator = decorator(decorator)

@decorator
def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    return n_ary_f

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            result = f(*args)
            cache[args] = result
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(*args)
    _f.cache = cache  # add a attrbute `cache` to `_f`, can be removed since cache is in the env in closure
    return _f

if __name__ == '__main__':  # test memo
    from trace_tool import countcalls,callcounts
    # print "init callcounts:",callcounts

    @countcalls
    @memo
    def fib_memo(n): return 1 if n<=1 else fib_memo(n-1)+fib_memo(n-2)

    @countcalls
    def fib(n): return 1 if n<=1 else fib(n-1)+fib(n-2)

    def test(n=10,f=fib):
        print"function name:\t",f.__name__
        print("   n    result   callcounts")
        print("----------------------------")
        for i in range(1,n+1):
            print "%4d %8d %8d"%(i, f(i), callcounts[f])
            callcounts[fib]=0

    test()
    test(n=30,f=fib_memo)
