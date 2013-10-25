#! /usr/bin/env python
# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes
# a string as input and returns the i and j indices that
# correspond to the beginning and end indices of the longest
# palindrome in the string.
#
# Grading Notes:
#
# You will only be marked correct if your function runs
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

# def longest_subpalindrome_slice(text):
#     "Return (i, j) such that text[i:j] is the longest palindrome in text."
#     # Your code here
#     l = len(text)
#     r_max = 0
#     (low,up)=(i,j)=(0,0)
#     r=0
#     for m in range(l):
#         for r in range(min(m,l-m-1)):
#             print "(m,r,r_range):",(m,r,min(m,l-m-1))
#             (low,up)=(m-r,m+r)
#             if text[low]!=text[up]:
#                 if r>r_max:
#                     r_max = r
#                     (i,j)=(low+1,up-1)
#                 break
#         if r>r_max:
#             r_max = r
#             (i,j)=(low+1,up-1)
#     print (i,j)
#     print r_max
#     return (i,j)
#
#
# assert L('racecar') == (0, 7)


def longest_subpalindrome_slice(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    if text == '': return (0,0)
    text=text.lower()
    def length(slice):
        a,b = slice
        return b-a
    candidates = [grow(text,start,end)
                  for start in range(len(text))
                  for end in (start, start+1)]
    # print candidates
    return max(candidates, key=length)

def grow(text, start, end):
    "Start with a 0- or 1- length palindrome; try to grow a bigger one."
    while (start>0 and end<len(text)
           and text[start-1]==text[end]):
        start -= 1; end +=1
    return(start,end)

def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

if __name__ == '__main__':
    print test()
