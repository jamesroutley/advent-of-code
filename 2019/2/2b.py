#!/usr/bin/python3

"""
--- Part Two ---

"Good, the new computer seems to be working correctly! Keep it nearby during
this mission - you'll probably use it again. Real Intcode computers support
many more features than your new one, but we'll let you know what they are as
you need them."

"However, your current priority should be to complete your gravity assist
around the Moon. For this mission to succeed, we should settle on some
terminology for the parts you've already built."

Intcode programs are given as a list of integers; these values are used as the
initial state for the computer's memory. When you run an Intcode program, make
sure to start by initializing memory to the program's values. A position in
memory is called an address (for example, the first value in memory is at
"address 0").

Opcodes (like 1, 2, or 99) mark the beginning of an instruction. The values
used immediately after an opcode, if any, are called the instruction's
parameters. For example, in the instruction 1,2,3,4, 1 is the opcode; 2, 3, and
4 are the parameters. The instruction 99 contains only an opcode and has no
parameters.

The address of the current instruction is called the instruction pointer; it
starts at 0. After an instruction finishes, the instruction pointer increases
by the number of values in the instruction; until you add more instructions to
the computer, this is always 4 (1 opcode + 3 parameters) for the add and
multiply instructions. (The halt instruction would increase the instruction
pointer by 1, but it halts the program instead.)

"With terminology out of the way, we're ready to proceed. To complete the
gravity assist, you need to determine what pair of inputs produces the output
19690720."

The inputs should still be provided to the program by replacing the values at
addresses 1 and 2, just like before. In this program, the value placed in
address 1 is called the noun, and the value placed in address 2 is called the
verb. Each of the two input values will be between 0 and 99, inclusive.

Once the program has halted, its output is available at address 0, also just
like before. Each time you try a pair of inputs, make sure you first reset the
computer's memory to the values in the program (your puzzle input) - in other
words, don't reuse memory from a previous attempt.

Find the input noun and verb that cause the program to produce the output
19690720. What is 100 * noun + verb? (For example, if noun=12 and verb=2, the
answer would be 1202.)
"""

import fileinput
import typing


def run():
    lines = []
    for line in fileinput.input():
        lines.append(line)
    program = lines[0]
    for noun in range(99):
        for verb in range(99):
            output = compute(program, noun, verb)
            if output[0] == 19690720:
                return 100 * noun + verb


def compute(input: str, addr_1: int, addr_2: int) -> typing.List[int]:
    ast = parse(input)
    #  Get the program in the correct state, as per question
    ast[1] = addr_1
    ast[2] = addr_2
    result = evaluate(ast)
    return result


def parse(input: str) -> typing.List[int]:
    return [int(c) for c in input.split(",")]


def evaluate(ast: typing.List[int]) -> typing.List[int]:
    for i in range(0, len(ast) + 1, 4):
        opcode = ast[i]
        if opcode == 99:
            return ast
        if opcode == 1:
            a_pos = ast[i + 1]
            b_pos = ast[i + 2]
            a = ast[a_pos]
            b = ast[b_pos]
            loc = ast[i + 3]
            ast[loc] = a + b
        if opcode == 2:
            a_pos = ast[i + 1]
            b_pos = ast[i + 2]
            a = ast[a_pos]
            b = ast[b_pos]
            loc = ast[i + 3]
            ast[loc] = a * b
    raise Exception("Exit opcode not hit")


def _test_compute():
    assert compute("1,0,0,0,99") == [2, 0, 0, 0, 99]
    assert compute("2,3,0,3,99") == [2, 3, 0, 6, 99]
    assert compute("2,4,4,5,99,0") == [2, 4, 4, 5, 99, 9801]
    assert compute("1,1,1,4,99,5,6,0,99") == [30, 1, 1, 4, 2, 5, 6, 0, 99]


if __name__ == "__main__":
    # _test_compute()
    print(run())
