#! /usr/bin/env python

import sys
from collections import defaultdict

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

garden = defaultdict(lambda: '.')
max_y = len(lines)
for y,l in enumerate(lines):
    max_x = len(l)
    for x,c in enumerate(l):
        garden[x+y*1j] = c


def calc_regions():
    queue = [ set((z,)) for z in garden ]
    already_seen = set()
    regions = []

    while queue:
        region = queue.pop()

        if not region or region < already_seen:
            continue

        already_seen |= region

        new_region = set()
        for pos in region:
            for new_pos in set((pos+1, pos-1, pos+1j, pos-1j))-already_seen:
                if garden[pos] == garden[new_pos]:
                    new_region.add(new_pos)

        if new_region - region:
            queue.append(new_region|region)
        else:
            regions.append(region)

    return regions

regions = calc_regions()

def calc_perimeter(z):
    return sum(garden[z+d]!=garden[z] for d in (1,-1,1j, -1j))

print("Part 1:", sum(sum(calc_perimeter(z) for z in region)*len(region) for region in regions))


def calc_sides(reg):
    # In fact, we're counting corners...
    corners = 0
    for z in reg:
        corners += z-1 not in reg and z-1j not in reg
        corners += z+1 not in reg and z-1j not in reg
        corners += z-1 not in reg and z+1j not in reg
        corners += z+1 not in reg and z+1j not in reg

        corners += z-1 in reg and z-1j in reg and z-1-1j not in reg
        corners += z+1 in reg and z-1j in reg and z+1-1j not in reg
        corners += z-1 in reg and z+1j in reg and z-1+1j not in reg
        corners += z+1 in reg and z+1j in reg and z+1+1j not in reg

    return corners

print("Part 2:", sum(calc_sides(region)*len(region) for region in regions))
