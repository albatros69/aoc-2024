#! /usr/bin/env python

from fractions import Fraction
import sys
from heapq import heappop, heappush

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

claw_machines = []
current_config = {}
for l in lines:
    if l:
        what, rest = l.split(': ')
        if what.startswith("Button"):
            X,Y = (int(w[2:]) for w in rest.split(', '))
            current_config[what[-1]] = X+Y*1j
        elif what.startswith("Prize"):
            X,Y = (int(w[2:]) for w in rest.split(', '))
            current_config["prize"] = X+Y*1j
    elif not l and current_config:
        claw_machines.append(current_config)
        current_config = {}

if current_config:
    claw_machines.append(current_config)


def win_prize_p1(cfg: dict):
    queue = [(abs(cfg["prize"]), 0, 0, 0, cfg["prize"])]
    already_seen = set()

    while queue:
        d, cost, A, B, pos = heappop(queue)

        if d == 0:
            return cost

        if (A,B) in already_seen or A > 100 or B > 100:
            continue
        already_seen.add((A,B))

        new_pos_A = pos - cfg['A']
        new_pos_B = pos - cfg['B']
        if (A+1, B) not in already_seen:
            heappush(queue, (abs(new_pos_A), cost+3, A+1, B, new_pos_A))
        if (A, B+1) not in already_seen:
            heappush(queue, (abs(new_pos_B), cost+1, A, B+1, new_pos_B))

    return 0

print("Part 1:", sum(win_prize_p1(cfg) for cfg in claw_machines))


def win_prize_p2(cfg: dict):
    # Mathematics at our rescue...
    A: complex = cfg["A"]
    B: complex = cfg["B"]
    P: complex = cfg["prize"]

    det = -int((A*B.conjugate()).imag)
    if det == 0:
        return 0

    sol = Fraction(int(B.imag*P.real-B.real*P.imag), det), Fraction(int(A.real*P.imag-A.imag*P.real), det)
    if all(x.denominator == 1 for x in sol):
        return 3*sol[0] + sol[1]

    return 0


print("Part 1 (bis):", sum(win_prize_p2(cfg) for cfg in claw_machines))

for cfg in claw_machines:
    cfg["prize"] += 10000000000000*(1+1j)

print("Part 2:", sum(win_prize_p2(cfg) for cfg in claw_machines))
