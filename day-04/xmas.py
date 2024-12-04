#! /usr/bin/env python

import sys
from collections import defaultdict

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

xwords = defaultdict(lambda: '.')
for y,l in enumerate(lines):
    for x,c in enumerate(l):
        xwords[x+y*1j] = c

def neighbors(z: complex):
    seqs = (
        tuple(z+i        for i in range(4)),
        tuple(z+i*1j     for i in range(4)),
        tuple(z-i        for i in range(4)),
        tuple(z-i*1j     for i in range(4)),
        tuple(z+i*(1+1j) for i in range(4)),
        tuple(z-i*(1+1j) for i in range(4)),
        tuple(z+i*(1-1j) for i in range(4)),
        tuple(z-i*(1-1j) for i in range(4)),
    )
    return [''.join(xwords[z] for z in s) for s in seqs ]

all_X = [ z for z in xwords if xwords[z] == 'X' ]
print("Part 1:", sum(w == 'XMAS' for z in all_X for w in neighbors(z)))

def is_X_MAS(z: complex):
    seqs = (z+1+1j, z, z-1-1j), (z+1-1j, z, z-1+1j)
    return all(w=='MAS' or w[::-1]=='MAS' for w in (''.join(xwords[z] for z in s) for s in seqs))

all_A = [ z for z in xwords if xwords[z] == 'A' ]
print("Part 2:", sum(is_X_MAS(z) for z in all_A))
