"""
Advent Of Code 2022 Day 8
"""

from __future__ import annotations


from typing import Iterable
from dataclasses import dataclass
from pathlib import Path


input_dir = Path(__file__).parent.parent.parent / "input"


@dataclass
class Tree:
    height: int
    visible: bool = False
    scenic_score: int = 1


def viewing_distance(tree_line: Iterable[Tree]) -> int:
    highest_tree = -1
    new_visibles = 0

    height_to_closest_idx = [0] * 10
    for index, tree in enumerate(tree_line):
        # Part 1
        if not tree.visible and tree.height > highest_tree:
            tree.visible = True
            new_visibles += 1
        highest_tree = max(tree.height, highest_tree)

        # Part 2
        idx_of_blocking_tree = max(height_to_closest_idx[tree.height :])
        tree.scenic_score *= index - idx_of_blocking_tree
        height_to_closest_idx[tree.height] = index

    return new_visibles


def p1p2(input_file: Path = input_dir / "d08") -> tuple[int, int]:
    p1 = 0
    rows: list[list[Tree]] = []
    cols: list[list[Tree]] = []
    for input_line in input_file.read_text().splitlines():
        rows.append([Tree(int(char)) for char in input_line])
    for idx in range(len(rows)):
        cols.append([row[idx] for row in rows])

    # Go through each row forwards and backwards to calculate looking left and looking right distances
    # Similar for columns (up and down)
    for lines in (
        rows,
        (reversed(row) for row in rows),
        cols,
        (reversed(col) for col in cols),
    ):
        for line in lines:
            p1 += viewing_distance(line)

    p2 = max(tree.scenic_score for row in rows for tree in row)

    return (p1, p2)
