"""
Advent Of Code 2022 d04
"""

from __future__ import annotations


from pathlib import Path


repo_root = Path(__file__).parent.parent.parent


def range_to_set(range_str: str) -> set[int]:
    start, end = range_str.split("-")
    return set(range(int(start), int(end) + 1))


def p1p2(input_file: Path = repo_root / "input" / "d04-example") -> tuple[int, int]:
    p2 = 0
    num_subset_pairs = 0
    for line in input_file.read_text().splitlines():
        elf1, elf2 = line.split(",")

        elf1_set = range_to_set(elf1)
        elf2_set = range_to_set(elf2)
        if elf1_set.issubset(elf2_set) or elf2_set.issubset(elf1_set):
            num_subset_pairs += 1
        if not elf1_set.isdisjoint(elf2_set):
            p2 += 1

    return (num_subset_pairs, p2)
