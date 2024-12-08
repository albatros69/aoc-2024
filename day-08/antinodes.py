#! /usr/bin/env python

import sys
from collections import defaultdict
from itertools import product
from math import gcd

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

antennas = defaultdict(list)
max_y = len(lines)
for y, l in enumerate(lines):
    max_x = len(l)
    for x, c in enumerate(l):
        if c != '.':
            antennas[c].append(x+y*1j)

def antinodes_p1(a1: complex, a2: complex) -> set:
    if a1 == a2:
        return set()

    return set(
        z for z in (2*a2 - a1, 2*a1 - a2)
        if 0 <= z.real < max_x and 0 <= z.imag < max_y
    )

result = set().union(
    *(antinodes_p1(a, b) for c in antennas for (a, b) in product(antennas[c], repeat=2))
)
print("Part 1:", len(result))

def antinodes_p2(a1: complex, a2: complex) -> set:
    if a1 == a2:
        return set()

    vect = a2 - a1
    vect /= gcd(int(vect.real), int(vect.imag))

    result = set()
    z = a1
    while 0 <= z.real < max_x and 0 <= z.imag < max_y:
        result.add(z)
        z += vect
    z = a1
    while 0 <= z.real < max_x and 0 <= z.imag < max_y:
        result.add(z)
        z -= vect
    return result

result = set().union(
    *(antinodes_p2(a, b) for c in antennas for (a, b) in product(antennas[c], repeat=2))
)
print("Part 2:", len(result))
