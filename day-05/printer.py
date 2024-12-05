#! /usr/bin/env python

import sys
from collections import defaultdict
from functools import cmp_to_key

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

orders = defaultdict(list)
updates = []
for l in lines:
    try:
        a,b = l.split('|')
        orders[int(a)].append(int(b))
    except ValueError:
        if l:
            updates.append([int(a) for a in l.split(',')])

def is_correct(upd: list) -> bool:
    def is_in_order(a):
        try:
            idx = upd.index(a)
        except ValueError:
            return False

        for n in orders[a]:
            try:
                if idx > upd.index(n):
                    return False
            except:
                continue
        return True

    return all(is_in_order(b) for b in upd)

print("Part 1:", sum(u[len(u)//2] for u in updates if is_correct(u)))

def cmp(a: int,b:int):
    if b in orders[a]:
        return -1
    elif a in orders[b]:
        return 1
    else:
        return 0

result = 0
for upd in updates:
    if not is_correct(upd):
        upd.sort(key=cmp_to_key(cmp))
        result += upd[len(upd)//2]
print("Part 2:", result)

