"""
Advent Of Code 2022 Day 11
"""

from __future__ import annotations


import operator
from math import prod
from functools import partial
from collections import deque, Counter
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
    print(inspect_counts)
    return inspect_counts[-2] * inspect_counts[-1]


class ItemState(NamedTuple):
    worry: int
    monkey: int


def process_item(worry: int, monkey_num: int, num_monkeys: int,
                 common_mod: int, monkey_from_num: dict[int, Monkey],
                 worry_map: dict[ItemState, tuple[ItemState, int, int, ItemState]],
                 num_rounds: int) -> None:
    train_id = ItemState(worry, monkey_num)
    state = train_id
    per_round_inspects = []
    this_round_inspects = [0] * num_monkeys
    looped = False
    num_throws = 0
    while not looped:
        num_throws += 1
        this_round_inspects[state.monkey] += 1
        next_state_num = worry_map.get(state, None)
        throw_first_seen = None
        if next_state_num is None:
            this_monkey = monkey_from_num[state.monkey]
            next_worry = this_monkey.operation(state.worry) % common_mod
            next_monkey = (
                this_monkey.if_true_monkey
                if next_worry % this_monkey.test_div_by == 0
                else this_monkey.if_false_monkey
            )
            next_state = ItemState(next_worry, next_monkey)
        else:
            next_state, throw_first_seen, first_round_seen, train_to_see = next_state_num
            if train_to_see == train_id:
                looped = True
                # This appears to always happen on the last throw of a round - helpful?
        worry_map[state] = (next_state, num_throws, len(per_round_inspects), train_id)

        if next_state.monkey < state.monkey:
            # The next step will be on the next round
            per_round_inspects.append(this_round_inspects)
            this_round_inspects = this_round_inspects[:]  # cumulative
        else:
            assert not looped

        state = next_state

    # Loop hit
    head_round_len = first_round_seen + 1
    head_inspect_counts = per_round_inspects[head_round_len - 1]
    loop_round_len = len(per_round_inspects) - head_round_len
    loop_inspect_counts = []
    print(f"{train_id} hits loop after {throw_first_seen} throws ({head_round_len} rounds) "
          f"head. Loop length {num_throws - throw_first_seen} throws ({loop_round_len} rounds). ")
    for inspect_counts in per_round_inspects[head_round_len - 1:]:
        loop_inspect_counts.append(
            [loop_count - head_count for head_count, loop_count
             in zip(head_inspect_counts, inspect_counts)])
    loop_count, into_loop = divmod(num_rounds - head_round_len, loop_round_len)
    print(f"{loop_count=} {into_loop=} {len(loop_inspect_counts)=} {loop_round_len}")
    # head_inspect_counts + loop_inspect_counts[-1] * loop_count + loop_inspect_counts[into_loop]
    return [h + l + loop_count * l2 for h, l, l2 in zip(head_inspect_counts, loop_inspect_counts[into_loop], loop_inspect_counts[-1])]


def per_items(monkeys: list[Monkey]) -> int:
    monkey_from_num: dict[int, Monkey] = {m.number: m for m in monkeys}
    common_mod = prod([m.test_div_by for m in monkeys])
    worry_map: dict[ItemState, tuple[ItemState, int, int, ItemState]] = {}
    inspect_counts = [0] * len(monkeys)
    for monkey in monkeys:
        for worry, count in Counter(monkey.items).items():
            inspect_count_add = process_item(worry, monkey.number, len(monkeys),
                                             common_mod, monkey_from_num, worry_map, 10_000)
            inspect_counts = [old + count * new for old, new in zip(inspect_counts, inspect_count_add)]
    inspect_counts = sorted(inspect_counts)
    return inspect_counts[-2] * inspect_counts[-1]


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    input_lines = input_file.read_text().splitlines()
    monkeys = [
        Monkey.from_lines(input_lines[x : x + 7]) for x in range(0, len(input_lines), 7)
    ]
    init_states = [m.items.copy() for m in monkeys]
    print(f"{per_items(monkeys)=}")
    p1 = run_rounds(monkeys, div_3=True, rounds=20)

    # Reset monkeys for p2
    for m, init_items in zip(monkeys, init_states):
        m.items = init_items
        m.inspect_count = 0
        m.num_cache = {}

    p2 = run_rounds(monkeys, div_3=False, rounds=10_000)
    return (p1, p2)


if __name__ == "__main__":
    #print(p1p2(utils.example_input()))
    print(p1p2(utils.real_input()))
