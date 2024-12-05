#! /usr/bin/env python

import sys
import re

lines = []
for line in sys.stdin:
    lines.append(line.rstrip('\n'))

re_mul = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)')
correct_mul = sum((re_mul.findall(l) for l in lines), start=[])
#print(correct_mul)

print("Part 1:", sum(int(a)*int(b) for (a,b) in correct_mul))

re_mul_do = re.compile(r'mul\(([0-9]{1,3}),([0-9]{1,3})\)|(do|don\'t)\(\)')
correct_mul = sum((re_mul_do.findall(l) for l in lines), start=[])
#print(correct_mul)

enabled = True
result = 0
for a,b,switch in correct_mul:
    if switch == "do":
        enabled = True
    elif switch == "don't":
        enabled = False
    else:
        if enabled:
            result += int(a)*int(b)

print("Part 2:", result)

