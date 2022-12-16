"""
Advent Of Code 2022 Day 11
"""

from __future__ import annotations


import operator
from math import prod
from functools import partial
from collections import deque, Counter
from dataclasses import dataclass
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

    def next_monkey(self, test_worry: int) -> int:
        if test_worry % self.test_div_by == 0:
            return self.if_true_monkey
        else:
            return self.if_false_monkey


def run_rounds(monkeys: list[Monkey], rounds: int = 10_000) -> int:
    monkey_from_num: dict[int, Monkey] = {m.number: m for m in monkeys}

    for _ in range(rounds):
        for monkey in monkeys:
            while monkey.items:
                item_worry = monkey.items.popleft()
                monkey.inspect_count += 1
                worry = monkey.operation(item_worry) // 3
                next_monkey = monkey.next_monkey(worry)
                monkey_from_num[next_monkey].items.append(worry)
    inspect_counts = sorted(m.inspect_count for m in monkeys)
    return inspect_counts[-2] * inspect_counts[-1]


class ItemState(NamedTuple):
    worry: int
    monkey: int


def process_item(start_state: ItemState,
                 common_mod: int, num_to_monkey: dict[int, Monkey],
                 worry_map: dict[ItemState, tuple[ItemState, int, ItemState]],
                 num_rounds: int) -> list[int]:
    state = start_state
    per_round_inspects: list[list[int]] = []
    this_round_inspects = [0] * len(num_to_monkey)

    # Keep throwing the item from one Monkey to the next until it loops
    looped = False
    while not looped:
        this_round_inspects[state.monkey] += 1
        next_state_num = worry_map.get(state, None)
        if next_state_num is None:
            this_monkey = num_to_monkey[state.monkey]
            next_worry = this_monkey.operation(state.worry) % common_mod
            next_state = ItemState(
                next_worry, this_monkey.next_monkey(next_worry))
        else:
            next_state, first_round_seen, start_state_seen_by = next_state_num
            looped = (start_state_seen_by == start_state)

        worry_map[state] = (next_state, len(per_round_inspects), start_state)

        if next_state.monkey < state.monkey:
            # The next step will be on the next round
            per_round_inspects.append(this_round_inspects)
            this_round_inspects = this_round_inspects[:]  # cumulative
        else:
            # Any loop detected should always be at the end of a round
            # so if this isn't the end of a round, we shouldn't have looped
            assert not looped

        state = next_state

    # Now calculate how many rounds occured before the loop was hit
    head_round_len = first_round_seen + 1
    # ...and how many rounds it takes to go around the loop
    loop_len = len(per_round_inspects) - head_round_len

    # How many times will the item go around the loop
    loop_count, into_loop = divmod(num_rounds - head_round_len, loop_len)

    # The total inspect counts for this item is then the sum of
    #  - the inspect count increase around the loop multipled by times around the loop
    #  - the inspect count increase from a partial loop
    #  - the inspect count increase from the rounds before the loop
    # The sum of the last two is simply the inspect counts partway through the loop.
    inspect_count_over_loop = [end - start for end, start in zip(per_round_inspects[-1], per_round_inspects[head_round_len - 1])]
    partial_loop_inspect_counts = per_round_inspects[head_round_len + into_loop - 1]

    return [part_loop + loop_count * full_loop
            for part_loop, full_loop in zip(partial_loop_inspect_counts, inspect_count_over_loop)]


def process_each_item(num_to_monkey: dict[int, Monkey], rounds: int) -> int:
    """Process each item held until it hits a loop."""
    common_mod = prod([m.test_div_by for m in num_to_monkey.values()])
    worry_map: dict[ItemState, tuple[ItemState, int, ItemState]] = {}
    inspect_counts = [0] * len(num_to_monkey)
    for monkey in num_to_monkey.values():
        # Only calculate unique values - multiple the inspect counts by count
        for worry, count in Counter(monkey.items).items():
            item_inspect_counts = process_item(ItemState(worry, monkey.number),
                                               common_mod, num_to_monkey, worry_map, rounds)
            inspect_counts = [old + count * new for old, new in zip(inspect_counts, item_inspect_counts)]
    inspect_counts = sorted(inspect_counts)
    return inspect_counts[-2] * inspect_counts[-1]


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    input_lines = input_file.read_text().splitlines()
    monkeys = [Monkey.from_lines(input_lines[x : x + 7])
               for x in range(0, len(input_lines), 7)]
    num_to_monkey: dict[int, Monkey] = {m.number: m for m in monkeys}

    # Run p2 before p1 since p1 alters init state
    p2 = process_each_item(num_to_monkey, rounds=10_000)

    return (run_rounds(monkeys, rounds=20), p2)


if __name__ == "__main__":
    print(p1p2(utils.example_input()))
    print(p1p2(utils.real_input()))
