#! /usr/bin/env python

import sys
from dataclasses import dataclass, field

lines = []
for line in sys.stdin:
    lines.append(line.rstrip("\n"))


registers = {k: 0 for k in "ABC"}
program = None
for l in lines:
    if l.startswith("Register"):
        reg, val = l[9], int(l[12:])
        registers[reg] = val
    elif l.startswith("Program"):
        program = list(l[9:].split(","))

@dataclass
class Program:
    registers: dict
    program: tuple
    output: list[int] = field(default_factory=list)
    pointer: int = 0

    def combo(self, ope: str):
        match ope:
            case "0" | "1" | "2" | "3":
                return int(ope)
            case "4":
                return self.registers["A"]
            case "5":
                return self.registers["B"]
            case "6":
                return self.registers["C"]
            case _:
                raise ValueError

    def adv(self, ope: str):
        self.registers["A"] >>= self.combo(ope)
        self.pointer += 2

    def bxl(self, ope: str):
        self.registers["B"] ^= int(ope)
        self.pointer += 2

    def bst(self, ope: str):
        self.registers["B"] = self.combo(ope) & 7
        self.pointer += 2

    def jnz(self, ope: str):
        if self.registers["A"]:
            self.pointer = int(ope)
        else:
            self.pointer += 2

    def bxc(self, _):
        self.registers["B"] ^= self.registers["C"]
        self.pointer += 2

    def out(self, ope: str):
        self.output.append(str(self.combo(ope) & 7))
        self.pointer += 2

    def bdv(self, ope: str):
        self.registers["B"] = self.registers["A"] >> self.combo(ope)
        self.pointer += 2

    def cdv(self, ope: str):
        self.registers["C"] = self.registers["A"] >> self.combo(ope)
        self.pointer += 2

    def exec_opcode(self, opcode: str, operand: int):
        match opcode:
            case "0":
                return self.adv(operand)
            case "1":
                return self.bxl(operand)
            case "2":
                return self.bst(operand)
            case "3":
                return self.jnz(operand)
            case "4":
                return self.bxc(operand)
            case "5":
                return self.out(operand)
            case "6":
                return self.bdv(operand)
            case "7":
                return self.cdv(operand)
            case _:
                raise ValueError

    def run(self):
        while self.pointer < len(self.program):
            code, ope = self.program[self.pointer : self.pointer + 2]
            self.exec_opcode(code, ope)

    def pp_output(self) -> str:
        return ",".join(self.output)


p = Program(registers=registers.copy(), program=program)
p.run()
print("Part 1:", p.pp_output())

queue = [(0, 1)]
result = int(sys.maxsize)
while queue:
    val, idx = queue.pop(0)
    for a in range(val, val+8):
        p = Program(registers={"A": a, "B": 0, "C": 0}, program=program)
        p.run()
        if program[-idx:] == p.output:
            queue.append((a*8, idx+1))
            if idx == len(program):
                result = min(result, a)

print("Part 2:", result)


