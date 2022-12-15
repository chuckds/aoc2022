"""
Advent Of Code 2022 Day 11
"""

from __future__ import annotations


import operator
from math import prod
from functools import partial
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, NamedTuple

import utils


WorryOp = Callable[[int], int]


def func_str_to_callable(func_str: str) -> WorryOp:
    terms = func_str.split()
    if terms[1] == "*":
        if terms[2] == "old":
            return lambda x: x**2
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
    num_cache: dict[int, tuple[int, int]] = field(default_factory=dict)

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
    print(f"{common_mod=}")
    for _ in range(rounds):
        for monkey in monkeys:
            while monkey.items:
                item_worry = monkey.items.popleft()
                monkey.inspect_count += 1
                cache_info = monkey.num_cache.get(item_worry, None)
                if cache_info is None:
                    worry = monkey.operation(item_worry)
                    if div_3:
                        worry = worry // 3
                    else:
                        worry = worry % common_mod
                    dest_monkey = (
                        monkey.if_true_monkey
                        if worry % monkey.test_div_by == 0
                        else monkey.if_false_monkey
                    )
                    monkey.num_cache[item_worry] = (dest_monkey, worry)
                else:
                    dest_monkey, worry = cache_info

                monkey_from_num[dest_monkey].items.append(worry)
    inspect_counts = sorted(m.inspect_count for m in monkeys)

    return inspect_counts[-2] * inspect_counts[-1]


class ItemState(NamedTuple):
    worry: int
    monkey: int


def per_items(monkeys: list[Monkey]) -> None:
    monkey_from_num: dict[int, Monkey] = {m.number: m for m in monkeys}
    common_mod = prod([m.test_div_by for m in monkeys])
    worry_map: dict[ItemState, ItemState] = {}
    for monkey in monkeys:
        for worry in monkey.items:
            train_id = ItemState(worry, monkey.number)
            state = train_id
            per_round_inspects = []
            this_round_inspects = [0] * len(monkeys)
            looped = False
            in_cache = False
            while True:
                this_round_inspects[state.monkey] += 1
                next_state = worry_map.get(state, None)
                if next_state is None:
                    this_monkey = monkey_from_num[state.monkey]
                    next_worry = this_monkey.operation(state.worry) % common_mod
                    next_monkey = (
                        this_monkey.if_true_monkey
                        if next_worry % this_monkey.test_div_by == 0
                        else this_monkey.if_false_monkey
                    )
                    next_state = ItemState(next_worry, next_monkey)
                    worry_map[state] = next_state
                else:
                    in_cache = True

                looped = looped or next_state == train_id
                if next_state.monkey < state.monkey:
                    # The next step will be on the next round
                    per_round_inspects.append(this_round_inspects)
                    if looped or in_cache:
                        # End of round after looping so break
                        break
                    this_round_inspects = [0] * len(monkeys)
                elif looped or in_cache:
                    # We hit the cache but aren't at the end of a round
                    print(
                        f"{train_id} hit cycle ({looped} {in_cache}) after {len(per_round_inspects)} rounds but not at round end"
                    )

                state = next_state
            print(f"{train_id} {len(per_round_inspects)=} {len(worry_map)}")


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    input_lines = input_file.read_text().splitlines()
    monkeys = [
        Monkey.from_lines(input_lines[x : x + 7]) for x in range(0, len(input_lines), 7)
    ]
    init_states = [m.items.copy() for m in monkeys]
    per_items(monkeys)
    p1 = run_rounds(monkeys, div_3=True, rounds=20)

    # Reset monkeys for p2
    for m, init_items in zip(monkeys, init_states):
        m.items = init_items
        m.inspect_count = 0
        m.num_cache = {}

    p2 = run_rounds(monkeys, div_3=False, rounds=10_000)

    return (p1, p2)


if __name__ == "__main__":
    print(p1p2(utils.example_input()))
    print(p1p2(utils.real_input()))
