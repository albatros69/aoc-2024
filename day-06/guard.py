#! /usr/bin/env python

import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

x_map = {}
max_y = len(lines)
for y,l in enumerate(lines):
    max_x = len(l)
    for x,c in enumerate(l):
        x_map[x+y*1j] = c
        if c == '^':
            start = x+y*1j

x_map[start] = '.'

pos = start
dir = -1j
walk = set((start,))
try:
    while True:
        if x_map[pos+dir] == '.':
            pos += dir
            walk.add(pos)
        else:
            dir *= 1j
except KeyError:
    print("Part 1:", len(walk))

def guard_walk_loop(m: dict):
    p = start
    d = -1j
    w = { p: d }
    try:
        while True:
            if m[p+d] == '.':
                p += d
                if p in w and w[p] == d:
                    return True, len(w)
                w[p] = d
            else:
                d *= 1j
    except KeyError:
        return False, len(w)

print("Part 1 (bis):", guard_walk_loop(x_map)[1])

pos = start
dir = -1j
obstructions = set()
try:
    while True:
        if x_map[pos+dir] == '.':
            pos += dir

            new_map = x_map.copy()
            new_map[pos] = 'O'
            if guard_walk_loop(new_map)[0]:
                obstructions.add(pos)
                # for y in range(max_y):
                #     print(''.join(new_map[x+y*1j] for x in range(max_x)))
                # print('****')
        else:
            dir *= 1j
except KeyError:
    print("Part 2:", len(obstructions))
