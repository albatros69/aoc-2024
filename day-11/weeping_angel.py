#! /usr/bin/env python

import sys
from functools import cache

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

def change(n: int) -> list[int]:
    sn = str(n)
    if n == 0:
        return [1]
    elif len(sn) % 2 == 0:
        return [int(sn[:len(sn)//2]), int(sn[len(sn)//2:])]
    else:
        return [n*2024]

def new_step(st: list) -> list:
    new_st = []
    for n in st:
        new_st.extend(change(n))
    return new_st

stones = [int(w) for w in lines[0].split()]
for step in range(25):
    stones = new_step(stones)

print("Part 1:", len(stones))

@cache
def rec_change(n: int, steps):
    if steps == 0:
        return 1

    sn = str(n)
    if n == 0:
        return rec_change(1, steps-1)
    elif len(sn) % 2 == 0:
        return rec_change(int(sn[:len(sn)//2]), steps-1) + rec_change(int(sn[len(sn)//2:]), steps-1)
    else:
        return rec_change(2024*n, steps-1)

stones = [int(w) for w in lines[0].split()]
print("Part 1 (bis):", sum(rec_change(stone, 25) for stone in stones))
print("Part 2:", sum(rec_change(stone, 75) for stone in stones))
