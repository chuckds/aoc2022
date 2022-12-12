"""
Advent Of Code 2022 Day 10
"""

from __future__ import annotations


from pathlib import Path


input_dir = Path(__file__).parent.parent.parent / "input"


def p1p2(input_file: Path = input_dir / "real" / "d10") -> tuple[int, int]:
    p1, p2 = (0, 0)
    reg_x = 1
    cycle_count = 1
    next_strength_check = 20
    for line in input_file.read_text().splitlines():
        instruction, *values = line.split()
        x_inc = 0
        cycle_inst_start = cycle_count
        cycle_count += 1
        if instruction == "addx":
            x_inc = int(values[0])
            cycle_count += 1
        #print(f"{cycle_inst_start} {instruction} {x_inc} on {reg_x} -> {cycle_count} {reg_x + x_inc}")
        if cycle_count > next_strength_check:
            #print(f"{reg_x=} * {next_strength_check=} {reg_x * next_strength_check}")
            p1 += reg_x * next_strength_check
            next_strength_check += 40
        reg_x += x_inc

    return (p1, p2)
