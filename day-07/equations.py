#! /usr/bin/env python

import sys
import numpy as np

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

def solve_p1(numbers: list[int], total: int) -> bool:
    if not numbers:
        return False

    tmp = np.array(numbers[:1])
    for a in numbers[1:]:
        tmp = np.concatenate((a*tmp, a+tmp))

    return any(n==total for n in tmp)

def solve_p2(numbers: list[int], total: int) -> bool:
    if not numbers:
        return False

    tmp = np.array(numbers[:1])
    for a in numbers[1:]:
        tmp = np.concatenate((a*tmp, a+tmp, tmp*10**len(str(a))+a))

    return any(n==total for n in tmp)

result_p1, result_p2 = 0, 0
for l in lines:
    tmp = l.split()
    total = int(tmp[0][:-1])
    numbers = [ int(n) for n in tmp[1:]]
    result_p1 += total if solve_p1(numbers, total) else 0
    result_p2 += total if solve_p2(numbers, total) else 0
print("Part 1:", result_p1, "\nPart 2:", result_p2)
