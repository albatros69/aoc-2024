#! /usr/bin/env python

from collections import defaultdict
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

topomap = defaultdict(lambda: None)
for y,l in enumerate(lines):
    for x,c in enumerate(l):
        if c.isdigit():
            topomap[x+y*1j] = int(c)

def walk(start: complex):
    queue = [start]
    result_p1 = set()
    result_p2 = 0

    while queue:
        pos = queue.pop()

        if topomap[pos] == 9:
            result_p1.add(pos)
            result_p2 += 1
        else:
            queue.extend(
                p for p in (pos+1, pos-1, pos+1j, pos-1j) if topomap[p] is not None and topomap[p]-topomap[pos]==1
            )

    return len(result_p1), result_p2

tmp = [walk(p) for p in topomap.copy() if topomap[p]==0]
print("Part 1:", sum(a[0] for a in tmp))
print("Part 2:", sum(a[1] for a in tmp))
