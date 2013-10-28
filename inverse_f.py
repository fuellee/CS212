#! /usr/bin/env python
# --------------
# User Instructions
#
# Write a function, inverse, which takes as input a monotonically
# increasing (always increasing) function that is defined on the
# non-negative numbers. The runtime of your program should be
# proportional to the LOGARITHM of the input. You may want to
# do some research into binary search and Newton's method to
# help you out.
#
# This function should return another function which computes the
# inverse of the input function.
#
# Your inverse function should also take an optional parameter,
# delta, as input so that the computed value of the inverse will
# be within delta of the true value.

# -------------
# Grading Notes
#
# Your function will be called with three test cases. The
# input numbers will be large enough that your submission
# will only terminate in the allotted time if it is
# efficient enough.

def slow_inverse(f, delta=1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def f_1(y):
        x = 0
        while f(x) < y:
            x += delta
        # Now x is too big, x-delta is too small; pick the closest to y
        return x if (f(x)-y < y-f(x-delta)) else x-delta
    return f_1

def inverse(f, delta = 1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""

    def binary_search(low, high, goal_y):
        """low <= x <= high"""
        x = (low+high)/2.0
        y = f(x)
        while abs(y-goal_y)>delta:
            if y < goal_y:
                low = x
            else:
                high = x
            x = (low+high)/2.0
            y = f(x)
        return x

    def find_upper_bound(goal_y):
        """My first version.
        upper bound is too loose
        big `x` can cause `OverflowError` with float numbers
        (e.g. `power10(700.5)`)"""
        upbound = goal_y
        y = f(upbound)
        while(y < goal_y):
            upbound *= 2
            y = f(upbound)
        return upbound

    def find_bounds(goal_y):
        """find (low,high) that low <= y <= high
        Peter Norvig's version"""
        high = 1
        while(f(high)<goal_y):
            high *= 2
        low = 0 if (high==1) else high/2.0
        return (low,high)

    def reversed_f(y):
        # return binary_search(0,find_upper_bound(y),y)
        return binary_search(*find_bounds(y),goal_y=y)

    return reversed_f

if __name__ == '__main__':
    def square(x): return x*x
    sqrt = slow_inverse(square)

    def line(x): return x
    il = inverse(line)

    sqrt = inverse(square)

    def power10(x): return 10**x
    ln = inverse(power10)

    cuberoot = inverse(lambda x:x*x*x)

    def test1(n, name, value, expected):
        diff = abs(value-expected)
        print '%6g: %s = %13.7f (%13.7f actual); %.4f diff; %s' % (
            n, name, value, expected, diff,
            ('ok' if diff < 0.002 else '**** BAD ****'))
    def test():
        import math
        nums = map(lambda x:3**x, range(1,14))
        for n in nums:
            test1(n, 'sqrt', sqrt(n), math.sqrt(n))
            test1(n, 'ln  ', ln(n), math.log10(n))
            test1(n, '3-rt', cuberoot(n), n**(1.0/3.0))

    test()

