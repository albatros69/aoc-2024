#! /usr/bin/env python

import sys
from heapq import heappop, heappush

lines = []
for line in sys.stdin:
    lines.append(line.rstrip("\n"))

maxi, limit = 70, 1024
corrupted_memory = set()
for l in lines[:limit]:
    x, y = (int(n) for n in l.split(","))
    corrupted_memory.add((x, y))


def shortest_path():
    queue = [
        (
            0,
            0,
            0,
            frozenset(
                (0, 0),
            ),
        )
    ]
    already_seen = corrupted_memory.copy()

    while queue:
        l, x, y, path = heappop(queue)

        if (x, y) == (maxi, maxi):
            return l, path

        if not (0 <= x <= maxi and 0 <= y <= maxi) or (x, y) in already_seen:
            continue

        already_seen.add((x, y))
        for new_x, new_y in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if (
                0 <= new_x <= maxi
                and 0 <= new_y <= maxi
                and (new_x, new_y) not in already_seen
            ):
                heappush(
                    queue,
                    (
                        l + 1,
                        new_x,
                        new_y,
                        path | {(new_x, new_y)},
                    ),
                )

    return None, None


steps, path = shortest_path()
print("Part 1:", steps)

for l in lines[limit:]:
    x, y = (int(n) for n in l.split(","))
    corrupted_memory.add((x, y))

    if (x, y) in path:
        steps, path = shortest_path()
        if path is None:
            print("Part 2:", f"{x},{y}")
            break
