"""
Advent Of Code 2022 XXX
"""

from __future__ import annotations


from pathlib import Path


input_dir = Path(__file__).parent.parent.parent / "input"


def p1p2(input_file: Path = input_dir / "XXX-example") -> tuple[int, int]:
    p1, p2 = (0, 0)
    for line in input_file.read_text().splitlines():
        pass
    return (p1, p2)
