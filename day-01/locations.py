#! /usr/bin/env python

import sys
from collections import Counter

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

lefts, rights = [], []
for line in lines:
    l, r = [ int(n) for n in line.split() ]
    lefts.append(l)
    rights.append(r)

lefts.sort()
rights.sort()
print("Part 1:", sum(abs(a-b) for a,b in zip(lefts, rights)))

count_rights = Counter(rights)
print("Part 2:", sum(a*count_rights.get(a, 0) for a in lefts))

