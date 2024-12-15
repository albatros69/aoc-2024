#! /usr/bin/env python

import sys
from math import prod
from itertools import product

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

max_x, max_y = 101, 103

robots = []
for l in lines:
    robot = {}
    pos, vit = l.split()
    robot.update(zip('xy', (int(n) for n in pos[2:].split(','))))
    robot.update(zip(('vx', 'vy'), (int(n) for n in vit[2:].split(','))))
    robots.append(robot)


def safetly_level(nb_sec):
    quadrants = dict(zip(product((True, False), repeat=2), (0,)*4))

    for r in robots:
        rob_x = (r['x'] + nb_sec*r['vx'])%max_x
        rob_y = (r['y'] + nb_sec*r['vy'])%max_y

        if 0 <= rob_x < max_x//2 and 0 <= rob_y < max_y//2:
            quadrants[True, True] += 1
        elif 0 <= rob_x < max_x//2 and max_y//2+1 <= rob_y < max_y:
            quadrants[True, False] += 1
        elif max_x//2+1 <= rob_x < max_x and 0 <= rob_y < max_y//2:
            quadrants[False, True] += 1
        elif max_x//2+1 <= rob_x < max_x and max_y//2+1 <= rob_y < max_y:
            quadrants[False, False] += 1

    return prod(quadrants.values())

print("Part 1:", safetly_level(100))

# When the picture of the Christmas tree is formed, the robots are mostly in one quadrant,
# and the safety level is low. Thanks Reddit!
# https://www.reddit.com/r/adventofcode/comments/1he0g67/2024_day_14_part_2_the_clue_was_in_part_1/
runs = [safetly_level(n) for n in range(10000)]
print("Part 2:", runs.index(min(runs)))
