"""
Advent Of Code 2022 Day 17
"""

from __future__ import annotations


from pathlib import Path
from typing import NamedTuple, TypeVar, Iterator
from itertools import islice

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

move_down = Point(0, -1)


def cycle_list(a_list: list[T]) -> Iterator[T]:
    while True:
        for elem in a_list:
            yield elem


def check_move(
    shape: list[Point], move: Point, blocked: set[Point]
) -> tuple[bool, list[Point]]:
    new_pos = move.add_to_list(shape)
    if all(p not in blocked and 0 <= p.x < chamber_width and p.y >= 0 for p in new_pos):
        # No collision move is good
        return True, new_pos
    else:
        return False, shape


def stack_surface_simple(chamber_profile: list[int], col_contig_depth: list[int]) -> bool:
    c_h_d = zip(chamber_profile, col_contig_depth)
    for (col_height, col_depth), (next_col_height, next_col_depth) in zip(c_h_d, islice(c_h_d, 1)):
        relevant_depth = col_depth if col_height > next_col_height else next_col_depth
        if abs(col_height - next_col_height) > relevant_depth:
            return False
    return True


def update_per_column_info(shape: list[Point], col_heights: list[int], col_contig_depth: list[int]) -> None:
    for p in shape:
        if p.y > col_heights[p.x]:
            col_heights[p.x] = p.y
            if p.y > col_heights[p.x] + 1:
                # there's a gap
                col_contig_depth[p.x] = 1
            else:
                # Contiguous with previous content
                col_contig_depth[p.x] += 1
        else:
            # Filled in a gap!
            pass


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, ...]:
    moves: list[Point] = []
    for line in input_file.read_text().splitlines():
        moves = [move_map[char] for char in line]

    total_rocks = (2022, 1_000_000_000_000)
    move_gen, shape_gen = cycle_list(moves), cycle_list(shapes)
    highest_rock = -1
    col_heights = [-1] * chamber_width
    col_contig_depth = [0] * chamber_width
    blocked: set[Point] = set()
    move_count = 0
    column_states: dict[tuple[tuple[int, ...], int, int], int] = {}
    per_rock_heights = []
    for rock_count in range(max(total_rocks)):
        shape_start = Point(2, highest_rock + 4)
        shape_pos = shape_start.add_to_list(next(shape_gen)[:])
        per_rock_heights.append(highest_rock)

        falling = True
        while falling:
            _, shape_pos = check_move(shape_pos, next(move_gen), blocked)
            move_count += 1
            falling, shape_pos = check_move(shape_pos, move_down, blocked)

        # Shape has stopped falling
        blocked.update(shape_pos)

        # Now determine the state of the column
        update_per_column_info(shape_pos, col_heights, col_contig_depth)
        highest_rock = max(col_heights)
        min_height = min(col_heights)
        chamber_profile = [c - min_height for c in col_heights]
        if stack_surface_simple(chamber_profile, col_contig_depth):
            # Remember this state since it is sealed
            state_id = (tuple(chamber_profile), rock_count % len(shapes), move_count % len(moves))
            prev_rock_count = column_states.get(state_id, None)
            if prev_rock_count is not None:
                prev_height = per_rock_heights[prev_rock_count + 1]
                loop_len = rock_count - prev_rock_count
                loop_height_gain = highest_rock - prev_height
                answers = []
                for total_rock in total_rocks:
                    loops_to_do, into_loop = divmod(total_rock - rock_count - 1, loop_len)
                    answers.append(highest_rock + loop_height_gain * loops_to_do + per_rock_heights[prev_rock_count + into_loop + 1] - prev_height + 1)
                break
            else:
                column_states[state_id] = rock_count

    return tuple(answers)


if __name__ == "__main__":
    example = p1p2(utils.example_input())
    print(f"{example=}")
    real = p1p2(utils.real_input())
    print(f"{real=}")
    assert example == utils.get_day_result(True) and real == utils.get_day_result(False), "Answers wrong"
