#! /usr/bin/env python

from dataclasses import dataclass
import sys

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

warehouse_ori = {}
max_y = 0
moves = ''
robot_start = 0
for y,l in enumerate(lines):
    if l and l[0] == '#':
        max_y += 1
        max_x = len(l)
        for x,c in enumerate(l):
            warehouse_ori[x+y*1j] = c
            if c == '@':
                robot_start = x+y*1j
    elif l:
        moves += l

# warehouse = warehouse_ori.copy()

# print(moves)
# for y in range(max_y):
#     print(''.join(warehouse_ori[x+y*1j] for x in range(max_x)))


@dataclass
class Robot_p1:
    warehouse: dict
    pos: complex

    def convert_dir(self, dir: str):
        return {'^': -1j, 'v': 1j, '>': 1, '<': -1}[dir]

    def goods(self, dir: complex):
        result = []
        pos = self.pos + dir
        while self.warehouse[pos] == 'O':
            result.append(pos)
            pos += dir

        return result[::-1], self.warehouse[pos]

    def move(self, dir: str):

        d = self.convert_dir(dir)
        goods, c = self.goods(d)

        if c == '.':
            for g in goods:
                self.warehouse[g+d] = self.warehouse[g]

            self.warehouse[self.pos] = '.'
            self.pos += d
            self.warehouse[self.pos] = '@'

    def gps(self):
        return int(sum(z.real + 100*z.imag for z,c in self.warehouse.items() if c=='O'))

r = Robot_p1(warehouse_ori.copy(), robot_start)
for m in moves:
    r.move(m)
    # print("***", m, "***")
    # for y in range(max_y):
    #     print(''.join(r.warehouse[x+y*1j] for x in range(max_x)))

print("Part 1:", r.gps())

new_warehouse = {}
for z,c in warehouse_ori.items():
    new_warehouse[z+z.real] = '[' if c == 'O' else c
    if c == '@':
        c = '.'
    new_warehouse[z+z.real+1] = ']' if c == 'O' else c

robot_start += robot_start.real

# for y in range(max_y):
#     print(''.join(new_warehouse[x+y*1j] for x in range(2*max_x)))

class Robot_p2(Robot_p1):

    def goods(self, dir: complex):
        result = [self.pos]

        if dir.imag == 0:
            pos = self.pos + dir
            while self.warehouse[pos] in '[]':
                result.append(pos)
                pos += dir
            if self.warehouse[pos] == '#':
                return []

        elif dir.real == 0:
            pos = [self.pos]
            new_pos = True
            while new_pos:
                new_pos = set()
                for p in (p+dir for p in pos):
                    if self.warehouse[p] == '[':
                        new_pos.update((p,p+1))
                    elif self.warehouse[p] == ']':
                        new_pos.update((p-1,p))
                    elif self.warehouse[p] == '.':
                        pass
                    elif self.warehouse[p] == '#':
                        return []

                pos = new_pos
                result.extend(new_pos)

        return result[::-1]


    def move(self, dir: str):

        d = self.convert_dir(dir)
        goods = self.goods(d)

        if goods:
            for g in goods:
                self.warehouse[g+d] = self.warehouse[g]
                self.warehouse[g] = '.'

            self.pos += d

    def gps(self):
        return int(sum(z.real + 100*z.imag for z,c in self.warehouse.items() if c=='['))

r = Robot_p2(new_warehouse, robot_start)
for i,m in enumerate(moves):
    r.move(m)
    # print("***", i, m, "***")
    # for y in range(max_y):
    #     print(''.join(r.warehouse[x+y*1j] for x in range(2*max_x)))

print("Part 2:", r.gps())

