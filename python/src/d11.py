"""
Advent Of Code 2022 d11
"""

from __future__ import annotations


from collections import deque
from dataclasses import dataclass
from pathlib import Path


input_dir = Path(__file__).parent.parent.parent / "input"


@dataclass
class Monkey:
    number: int
    items: deque[int]
    operation: str
    test_div_by: int
    if_true_monkey: int
    if_false_monkey: int
    inspect_count: int = 0

    @classmethod
    def from_lines(cls, lines: list[str]) -> Monkey:
        return cls(
            int(lines[0].split()[1][:-1]),
            deque([int(x) for x in lines[1].split(":")[1].split(",")]),
            lines[2].split(" =")[1],
            int(lines[3].split(" by ")[1]),
            int(lines[4].split()[-1]),
            int(lines[5].split()[-1]),
        )


def p1p2(input_file: Path = input_dir / "real" / "d11") -> tuple[int, int]:
    p2 = 0
    input_lines = input_file.read_text().splitlines()
    monkeys = [Monkey.from_lines(input_lines[x:x + 7]) for x in range(0, len(input_lines), 7)]
    monkey_from_num: dict[int, Monkey] = {m.number: m for m in monkeys}
    for _ in range(20):
        for monkey in monkeys:
            while monkey.items:
                item_worry = monkey.items.popleft()
                monkey.inspect_count += 1
                old = item_worry
                worry = eval(monkey.operation)
                worry = worry // 3
                if worry % monkey.test_div_by == 0:
                    monkey_from_num[monkey.if_true_monkey].items.append(worry)
                else:
                    monkey_from_num[monkey.if_false_monkey].items.append(worry)

    inspect_counts = sorted(m.inspect_count for m in monkeys)
    return (inspect_counts[-2] * inspect_counts[-1], p2)
