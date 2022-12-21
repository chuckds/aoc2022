"""
Advent Of Code 2022 Day 17
"""

from __future__ import annotations


from pathlib import Path
from typing import NamedTuple, TypeVar, Iterable, Iterator

import utils


T = TypeVar("T")


class Point(NamedTuple):
    x: int
    y: int

    def add_to_list(self, shape: list[Point]) -> list[Point]:
        return [Point(self.x + p.x, self.y + p.y) for p in shape]


# Y increases bottom to top
# X left to right
# A shape is a list of points that are blocked from bottom left of shape being 0,0
shapes = [
    [Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)],  # Horiz line
    [Point(0, 1), Point(1, 0), Point(1, 1), Point(1, 2), Point(2, 1)],  # Cross
    [Point(0, 0), Point(1, 0), Point(2, 0), Point(2, 1), Point(2, 2)],  # L
    [Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)],  # Vert line
    [Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)],  # Square
]

move_map = {
    ">": Point(1, 0),
    "<": Point(-1, 0),
}

chamber_width = 7


def cycle_list(a_list: list[T]) -> Iterator[T]:
    while True:
        for elem in a_list:
            yield elem


def check_move(shape: list[Point], move: Point, blocked: set[Point]) -> tuple[bool, list[Point]]:
    new_pos = move.add_to_list(shape)
    if all(p not in blocked and 0 <= p.x < chamber_width and p.y >= 0 for p in new_pos):
        # No collision move is good
        return True, new_pos
    else:
        return False, shape


def print_blocked(blocked: set[Point], highest_rock: int) -> None:
    for row in range(highest_rock, -1, -1):
        for col in range(chamber_width):
            if Point(col, row) in blocked:
                print("#", end="")
            else:
                print(".", end="")
        print()


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    p1, p2 = (0, 0)

    moves: list[Point] = []
    for line in input_file.read_text().splitlines():
        moves = [move_map[char] for char in line]

    move_gen, shape_gen = cycle_list(moves), cycle_list(shapes)
    down = Point(0, -1)
    highest_rock = -1
    col_heights = [-1] * chamber_width
    blocked: set[Point] = set()
    rock_count = 0
    total_rocks = 1_000_000_000_000
    total_rocks = 2022
    while rock_count < total_rocks:
        shape_start = Point(2, highest_rock + 4)
        shape_pos = shape_start.add_to_list(next(shape_gen)[:])
        rock_count += 1

        falling = True
        while falling:
            _, shape_pos = check_move(shape_pos, next(move_gen), blocked)
            falling, shape_pos = check_move(shape_pos, down, blocked)

        # Shape has stopped falling
        highest_rock = max(highest_rock, max(p.y for p in shape_pos))
        if rock_count == 2022:
            p1 = highest_rock + 1
        for p in shape_pos:
            if p.y > col_heights[p.x]:
                col_heights[p.x] = p.y
        min_c = min(col_heights)
        print(" ".join([f"{h - min_c:03}" for h in col_heights]))
        blocked.update(shape_pos)

    return (p1, highest_rock)


if __name__ == "__main__":
    print(p1p2(utils.example_input()))
    print(p1p2(utils.real_input()))
