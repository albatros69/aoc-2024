#! /usr/bin/env python

import sys
from dataclasses import dataclass
from itertools import islice


def batched(iterable, n):
    # batched('ABCDEFG', 3) → ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch


lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

@dataclass
class File:
    size: int
    id: int
    pos: int

class FileSystem:
    nb_blocks: int
    blocks: list
    fat: list

    def __init__(self, line: str):
        self.fat = []
        self.blocks = []
        self.nb_blocks = sum(int(n) for n in line)

        if len(line) % 2 != 0:
            line += '0'

        id = 0
        start = 0
        for fi,fr in batched(line, n=2):
            fi, fr = int(fi), int(fr)
            self.fat.extend([File(fi, id, start), File(fr, None, start+fi)])
            id += 1
            start += fi + fr

        for f in self.fat:
            self.blocks.extend((f.id, ) * f.size)

    def compact_p1(self):
        for i,b in enumerate(self.blocks[::-1]):
            free_b = self.blocks.index(None)
            if all(b is None for b in self.blocks[free_b:]):
                break
            self.blocks[free_b] = b
            self.blocks[-(1+i)] = None

    def find_free_space(self, f):
        start = -1
        while True:
            try:
                start = self.blocks.index(None, start+1, f.pos)
            except ValueError:
                break
            if self.blocks[start:start+f.size] == [None,]*f.size:
                return start
        return None

    def compact_p2(self):
        for f in self.fat[::-1]:
            if f.id is None:
                continue
            first_free_space = self.find_free_space(f)
            if first_free_space is None:
                continue
            self.blocks[f.pos:f.pos+f.size] = [None,]*f.size
            f.pos = first_free_space
            self.blocks[f.pos:f.pos+f.size] = [f.id,]*f.size
            # print(self.block_map())

    @property
    def checksum(self):
        return sum(i*b for i,b in enumerate(self.blocks) if b is not None)

    def block_map(self):
        return ''.join('.' if n is None else str(n) for n in self.blocks)



fs = FileSystem(lines[0])
fs.compact_p1()
print("Part 1:", fs.checksum)

fs = FileSystem(lines[0])
fs.compact_p2()
print("Part 2:", fs.checksum)

