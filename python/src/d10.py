"""
Advent Of Code 2022 Day 10
"""

from __future__ import annotations


from pathlib import Path


input_dir = Path(__file__).parent.parent.parent / "input"


CRT_WIDTH = 40


def draw_pixel(cycle: int, reg_x: int) -> str:
    pixel_being_drawn = (cycle - 1) % CRT_WIDTH
    result = "."
    if pixel_being_drawn - 1 <= reg_x <= pixel_being_drawn + 1:
        result = "#"

    if pixel_being_drawn == (CRT_WIDTH - 1):
        result += "\n"
    return result


def p1p2(input_file: Path = input_dir / "real" / "d10") -> tuple[int, str]:
    p1, p2 = (0, "")
    reg_x = 1
    cycle_count = 1
    next_strength_check = 20
    for line in input_file.read_text().splitlines():
        instruction, *values = line.split()
        x_inc = 0

        p2 += draw_pixel(cycle_count, reg_x)
        cycle_count += 1
        if instruction == "addx":
            x_inc = int(values[0])
            p2 += draw_pixel(cycle_count, reg_x)
            cycle_count += 1

        if cycle_count > next_strength_check:
            p1 += reg_x * next_strength_check
            next_strength_check += 40
        reg_x += x_inc

    return (p1, p2)
