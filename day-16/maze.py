#! /usr/bin/env python

import sys
from heapq import heappop, heappush

lines = []
for line in sys.stdin:
    lines.append(line.rstrip("\n"))

maze = {}
max_y = len(lines)
for y, l in enumerate(lines):
    max_x = len(l)
    for x, c in enumerate(l):
        if c == "S":
            start = (x, y)
            c = "."
        elif c == "E":
            end = (x, y)
        maze[x + y * 1j] = c


def best_path():
    queue = [(0, start, (1, 0))]
    already_seen = {}

    while queue:
        cost, (x, y), (dx, dy) = heappop(queue)
        pos = x + y * 1j
        d = dx + dy * 1j

        if maze[pos] == "E":
            return cost

        if maze[pos] == "#" or cost > already_seen.get((pos, d), cost + 1):
            continue

        already_seen[(pos, d)] = cost

        if maze[pos + d] != "#":
            new_pos = pos + d
            heappush(queue, (cost + 1, (new_pos.real, new_pos.imag), (dx, dy)))

        new_d = 1j * d
        heappush(queue, (cost + 1000, (x, y), (new_d.real, new_d.imag)))
        heappush(queue, (cost + 1000, (x, y), (-new_d.real, -new_d.imag)))

    return None


b_path = best_path()
print("Part 1:", b_path)


def best_tiles():
    queue = [(0, start, (1, 0), frozenset((complex(*start),)))]
    already_seen = {}
    result = set((complex(*start),))

    while queue:
        cost, (x, y), (dx, dy), tiles = heappop(queue)
        pos = x + y * 1j
        d = dx + dy * 1j

        if maze[pos] == "E" and cost == b_path:
            result.update(tiles)

        if (
            maze[pos] == "#"
            or cost > already_seen.get((pos, d), cost + 1)
            or cost > b_path
        ):
            continue

        already_seen[pos, d] = cost

        if maze[pos + d] != "#":
            new_pos = pos + d
            heappush(
                queue,
                (
                    cost + 1,
                    (new_pos.real, new_pos.imag),
                    (dx, dy),
                    tiles | frozenset((new_pos,)),
                ),
            )

        new_d = 1j * d
        new_cost = cost + 1000
        if new_cost < b_path and new_cost <= already_seen.get(
            (pos, new_d), new_cost + 1
        ):
            heappush(queue, (new_cost, (x, y), (new_d.real, new_d.imag), tiles))
            heappush(queue, (new_cost, (x, y), (-new_d.real, -new_d.imag), tiles))

    return result


tmp = best_tiles()
print("Part 2:", len(tmp))
