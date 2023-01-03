"""
Advent Of Code 2022 Day 24
"""

from __future__ import annotations


from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
from typing import NamedTuple, Iterator
from bisect import insort
import math

import utils


class Direction(Enum):
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    UP = (0, -1)


class Point(NamedTuple):
    x: int
    y: int

    def adjacents(self, limit: Point) -> Iterator[Point]:
        for dir in Direction:
            poss_point = Point(self.x + dir.value[0], self.y + dir.value[1])
            if 0 <= poss_point.x < limit.x and 0 <= poss_point.y < limit.y:
                yield poss_point


@dataclass
class Grid:
    dimentions: Point
    cycle: int = field(init=False)
    cell_blizzard_blocked: dict[Point, set[int]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.cycle = math.lcm(self.dimentions.x, self.dimentions.y)

    def add_blizzard(self, blizzard_posn: Point,
                     direction: Direction) -> None:
        posn = blizzard_posn
        limit = [g for g, d in zip(self.dimentions, direction.value) if d != 0][0]
        for min_mod in range(limit):
            self.cell_blizzard_blocked.setdefault(
                posn, set()).update(min_mod + cycle * limit
                                    for cycle in range(self.cycle // limit))
            posn = Point((posn.x + direction.value[0]) % self.dimentions.x,
                         (posn.y + direction.value[1]) % self.dimentions.y)

    def blizz_free_min(self, from_min: int, to_min: int, point: Point) -> set[int]:
        blocked_on = self.cell_blizzard_blocked.get(point, None)
        if blocked_on is None:
            blizz_min = set()  # No blizzard goes through this point
        else:
            blizz_min = set((x - from_min) % self.cycle for x in blocked_on
                            if ((x - from_min) % self.cycle) <= ((to_min - from_min - 1) % self.cycle))
        return set(range(to_min - from_min)) - blizz_min

    def min_till_blizzard(self, at_min: int, point: Point) -> int:
        blocked_on = self.cell_blizzard_blocked.get(point, None)
        if blocked_on is None:
            return self.cycle  # No blizzard goes through this point
        else:
            return min((x - at_min) % self.cycle for x in blocked_on)

    def dj(self, start: Point, start_min: int, end: Point) -> int:
        to_visit = [(0, (start, start_min))]
        visited = {}
        while to_visit:
            min_to_here, posn_id = to_visit.pop()
            if posn_id in visited:
                continue
            visited[posn_id] = min_to_here
            posn, min_mod_cycle = posn_id
            if posn == end:
                return min_to_here
            min_till_blizz = self.min_till_blizzard(min_mod_cycle, posn)
            for adj in posn.adjacents(self.dimentions):
                adj_blizz_free = self.blizz_free_min(min_mod_cycle + 1,
                                                     min_mod_cycle + min_till_blizz + 1, adj)
                for min in adj_blizz_free:
                    posn_id = (adj, (min_mod_cycle + 1 + min) % self.cycle)
                    if posn_id not in visited:
                        insort(to_visit, ((min_to_here + 1 + min, posn_id)), key=lambda x: -1 * x[0])
        return -2


char_to_dir = {
    ">": Direction.RIGHT,
    "v": Direction.DOWN,
    "<": Direction.LEFT,
    "^": Direction.UP,
}


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    p2 = 0
    blizzards: list[tuple[Point, Direction]] = []
    grid_width = 0
    start, dest = None, None
    for row_idx, line in enumerate(input_file.read_text().splitlines()):
        if not grid_width:
            grid_width = len(line) - 2
        for col_idx, char in enumerate(line):
            if char != "#" and start is None:
                start = Point(col_idx - 1, row_idx - 1)
            blizzard_dir = char_to_dir.get(char, None)
            if blizzard_dir is None:
                if char == ".":
                    # Aim for the cell above the exit - it's a simple move down to dest
                    dest = Point(col_idx - 1, row_idx - 2)
            else:
                blizzards.append((Point(col_idx - 1, row_idx - 1), blizzard_dir))

    assert start is not None and dest is not None
    grid = Grid(Point(grid_width, row_idx - 1))
    for blizzard_posn, blizzard_dir in blizzards:
        grid.add_blizzard(blizzard_posn, blizzard_dir)

    p1 = grid.dj(start, 0, dest) + 1  # Extra 1 to account for getting to the edge from dest
    if p1 == 18:
        back_to_start = grid.dj(Point(dest.x, dest.y + 1), p1 % grid.cycle, Point(start.x, start.y + 1)) + 1  # Extra 1 to account for getting to the edge from dest
        back_to_dest = grid.dj(start, (p1 + back_to_start) % grid.cycle, dest) + 1
        p2 = p1 + back_to_start + back_to_dest
    return (p1, p2)


if __name__ == "__main__":
    utils.per_day_main()
