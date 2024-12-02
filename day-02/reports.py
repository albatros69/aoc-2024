#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(list(int(n) for n in line.rstrip('\n').split()))

def is_safe(l: list, order: bool|None=None) -> bool:
    try:
        a,b,*_ = l
    except ValueError:
        return True

    if order is None:
        return 0 < abs(b-a) <= 3 and is_safe(l[1:], b-a>=0)
    if order:
        return 0 < b-a <= 3 and is_safe(l[1:], order)
    else:
        return 0 < a-b <= 3 and is_safe(l[1:], order)

print("Part 1:", sum(is_safe(l) for l in lines))

def dampener(l: list):
    return [ l[:i] + l[i+1:] for i in range(len(l)) ]

print("Part 2:", sum(any(is_safe(l) for l in dampener(li)) for li in lines))

