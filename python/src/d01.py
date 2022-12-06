"""
Advent Of Code 2022 Day 1
"""

import bisect
from pathlib import Path


repo_root = Path(__file__).parent.parent.parent


def p1p2(input_file: Path = repo_root / "input" / "d01-example") -> tuple[int, int]:
    current_sum = 0
    sorted_elves: list[int] = []
    for line in input_file.read_text().splitlines():
        if line:
            current_sum += int(line)
        else:
            bisect.insort(sorted_elves, current_sum)
            sorted_elves = sorted_elves[-3:]
            current_sum = 0
    bisect.insort(sorted_elves, current_sum)
    sorted_elves = sorted_elves[-3:]

    return (sorted_elves[-1], sum(sorted_elves))
