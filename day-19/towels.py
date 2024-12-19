#! /usr/bin/env python

import sys
from functools import cache

lines = []
for line in sys.stdin:
    lines.append(line.rstrip("\n"))

towels = lines[0].split(", ")
patterns = lines[2:]


@cache
def find(pattern: str):
    if not pattern:
        return 1

    return sum(find(pattern[len(t) :]) for t in towels if pattern.startswith(t))


tmp = [find(p) for p in patterns]
print("Part 1:", sum(a > 0 for a in tmp))
print("Part 2:", sum(a for a in tmp))
