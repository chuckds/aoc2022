#!/bin/env python3
"""
Advent Of Code 2022 d08
"""

from __future__ import annotations


from dataclasses import dataclass
from pathlib import Path


repo_root = Path(__file__).parent.parent.parent


@dataclass
class Tree:
    height: int
    visible: bool = False


def p1p2(input_file: Path = repo_root / "input" / "d08") -> tuple[int, int]:
    p1, p2 = (0, 0)
    rows, cols = [], []
    for input_line in input_file.read_text().splitlines():
        rows.append([Tree(int(char)) for char in input_line])
    for idx in range(len(rows)):
        cols.append([row[idx] for row in rows])

    for lines in (rows, (reversed(row) for row in rows),
                  cols, (reversed(col) for col in cols)):
        for line in lines:
            highest_tree = -1
            for tree in line:
                if not tree.visible and tree.height > highest_tree:
                    tree.visible = True
                    p1 += 1
                highest_tree = max(tree.height, highest_tree)
                if highest_tree == 9:
                    break

    return (p1, p2)
