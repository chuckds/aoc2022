"""
Advent Of Code 2022 Day 5
"""

from __future__ import annotations


from collections import deque
from typing import NamedTuple
from pathlib import Path

import utils


real = utils.real_input()


class Move(NamedTuple):
    num_move: int
    from_stack: int
    to_stack: int


def p1p2(input_file: Path = real) -> tuple[str, str]:
    p1, p2 = ("", "")

    stacks: dict[int, deque[str]] = {}
    moves: list[Move] = []
    stack_phase = True
    for line in input_file.read_text().splitlines():
        if stack_phase:
            for stack_num, stack_char in enumerate(line[1::4]):
                if stack_char == "1":
                    stack_phase = False
                    break
                elif stack_char != " ":
                    stacks.setdefault(stack_num + 1, deque()).appendleft(stack_char)
        elif line:
            tokens = line.split()
            moves.append(Move(*(int(tokens[i]) for i in (1, 3, 5))))

    p1stacks = {stack_num: stack.copy() for stack_num, stack in stacks.items()}
    for move in moves:
        for _ in range(move.num_move):
            p1stacks[move.to_stack].append(p1stacks[move.from_stack].pop())
        to_move = []
        for _ in range(move.num_move):
            to_move.append(stacks[move.from_stack].pop())
        to_move.reverse()
        stacks[move.to_stack].extend(to_move)

    for stack_num in range(1, len(stacks) + 1):
        p1 += p1stacks[stack_num].pop()
        p2 += stacks[stack_num].pop()
    return (p1, p2)
