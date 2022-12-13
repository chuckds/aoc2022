"""
Advent Of Code 2022 d11
"""

from __future__ import annotations


import operator
from math import prod
from functools import partial
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


input_dir = Path(__file__).parent.parent.parent / "input"


def square(x: int) -> int:
    return x**2


WorryOp = Callable[[int], int]


def func_str_to_callable(func_str: str) -> WorryOp:
    terms = func_str.split()
    if terms[1] == "*":
        if terms[2] == "old":
            return square
        else:
            return partial(operator.mul, int(terms[2]))
    else:  # terms[1] == "+"
        return partial(operator.add, int(terms[2]))


@dataclass
class Monkey:
    number: int
    items: deque[int]
    operation: WorryOp
    test_div_by: int
    if_true_monkey: int
    if_false_monkey: int
    inspect_count: int = 0

    @classmethod
    def from_lines(cls, lines: list[str]) -> Monkey:
        return cls(
            int(lines[0].split()[1][:-1]),
            deque([int(x) for x in lines[1].split(":")[1].split(",")]),
            func_str_to_callable(lines[2].split(" =")[1]),
            int(lines[3].split(" by ")[1]),
            int(lines[4].split()[-1]),
            int(lines[5].split()[-1]),
        )


def run_rounds(monkeys: list[Monkey], div_3: bool = False, rounds: int = 10_000) -> int:
    monkey_from_num: dict[int, Monkey] = {m.number: m for m in monkeys}

    common_mod = prod([m.test_div_by for m in monkeys])
    for _ in range(rounds):
        for monkey in monkeys:
            while monkey.items:
                item_worry = monkey.items.popleft()
                monkey.inspect_count += 1
                worry = monkey.operation(item_worry)
                if div_3:
                    worry = worry // 3
                else:
                    worry = worry % common_mod
                if worry % monkey.test_div_by == 0:
                    monkey_from_num[monkey.if_true_monkey].items.append(worry)
                else:
                    monkey_from_num[monkey.if_false_monkey].items.append(worry)
    inspect_counts = sorted(m.inspect_count for m in monkeys)
    return inspect_counts[-2] * inspect_counts[-1]


def p1p2(input_file: Path = input_dir / "real" / "d11") -> tuple[int, int]:
    input_lines = input_file.read_text().splitlines()
    monkeys = [
        Monkey.from_lines(input_lines[x : x + 7]) for x in range(0, len(input_lines), 7)
    ]
    init_states = [m.items.copy() for m in monkeys]
    p1 = run_rounds(monkeys, div_3=True, rounds=20)

    # Reset monkeys for p2
    for m, init_items in zip(monkeys, init_states):
        m.items = init_items
        m.inspect_count = 0

    p2 = run_rounds(monkeys, div_3=False, rounds=10_000)

    return (p1, p2)
