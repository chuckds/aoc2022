"""
Advent Of Code 2022 Day X
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import utils


real = utils.real_input()


def item_to_prio(item: str) -> int:
    offset = 96 if item.islower() else 38
    return ord(item) - offset


def p1p2(input_file: Path = real) -> tuple[int, int]:
    p1, p2 = (0, 0)
    group_unique_items: Counter[str] = Counter()
    for index, line in enumerate(input_file.read_text().splitlines()):
        comp1 = set(line[: len(line) // 2])
        comp2 = set(line[len(line) // 2 :])
        p1 += item_to_prio((comp1 & comp2).pop())
        group_unique_items.update(set(line))
        if index % 3 == 2:
            p2 += item_to_prio(group_unique_items.most_common(1)[0][0])
            group_unique_items = Counter()

    return (p1, p2)
