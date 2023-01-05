"""
Advent Of Code 2022 Day 24
"""

from __future__ import annotations


from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
from typing import NamedTuple, Iterator, Iterable
from bisect import insort, bisect_right, bisect_left
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
    cell_blizz_min: dict[Point, list[int]] = field(default_factory=dict)
    cell_free_min: dict[Point, list[int]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.cycle = math.lcm(self.dimentions.x, self.dimentions.y)

    def perf(self) -> None:
        for point, blizz_min in self.cell_blizzard_blocked.items():
            self.cell_blizz_min[point] = sorted(blizz_min)
        for point, blizz_min_sorted in self.cell_blizz_min.items():
            prev_min = 0
            point_free_min: list[int] = []
            for min in blizz_min_sorted:
                point_free_min.extend(range(prev_min, min))
                prev_min = min + 1
            point_free_min.extend(range(prev_min, self.cycle))
            self.cell_free_min[point] = point_free_min

    def add_blizzard(self, blizzard_posn: Point, direction: Direction) -> None:
        posn = blizzard_posn
        limit = [g for g, d in zip(self.dimentions, direction.value) if d != 0][0]
        for min_mod in range(limit):
            self.cell_blizzard_blocked.setdefault(posn, set()).update(
                min_mod + cycle * limit for cycle in range(self.cycle // limit)
            )
            posn = Point(
                (posn.x + direction.value[0]) % self.dimentions.x,
                (posn.y + direction.value[1]) % self.dimentions.y,
            )

    def blizz_free_min(self, from_min: int, to_min: int, point: Point) -> Iterable[int]:
        free_on = self.cell_free_min.get(point, None)
        for_min = (to_min - from_min - 1) % self.cycle + 1
        if free_on is None:  # No blizzards pass this point so always free
            for x in range(for_min):
                yield x
        else:
            idx = bisect_left(free_on, from_min)
            if idx == len(free_on):
                idx = 0  # wrap around
            for idx in range(idx, idx + len(free_on)):
                min_free = free_on[idx % len(free_on)]
                min_away = (min_free - from_min) % self.cycle
                if min_away < for_min:
                    yield min_away
                else:
                    break

    def next_min_with_blizz(self, at_min: int, point: Point) -> int:
        blocked_on = self.cell_blizz_min.get(point, None)
        if blocked_on is None:
            return at_min  # No blizzard goes through this point
        else:
            idx = bisect_right(blocked_on, at_min)
            return blocked_on[0] if idx == len(blocked_on) else blocked_on[idx]

    def dj(self, start: Point, start_min: int, end: Point) -> int:
        to_visit = [(0, (start, start_min))]
        visited = {}
        while to_visit:
            min_to_here, posn_id = to_visit.pop()
            if (
                posn_id in visited
            ):  # Must have been on to_visit multiple times - the first one will have been the quickest so discard
                continue
            visited[posn_id] = min_to_here
            posn, min_mod_cycle = posn_id
            if posn == end:
                return min_to_here
            next_blizz_min = self.next_min_with_blizz(min_mod_cycle, posn)

            # For each minute that we can wait here add that as the shortest path
            for min in range(1, (next_blizz_min - min_mod_cycle) % self.cycle):
                pos_id = (posn, (min_mod_cycle + min) % self.cycle)
                visited[pos_id] = min_to_here + min

            # For each adjacent cell visit it at each possible minute
            for adj in posn.adjacents(self.dimentions):
                for min in self.blizz_free_min(
                    min_mod_cycle + 1, next_blizz_min + 1, adj
                ):
                    posn_id = (adj, (min_mod_cycle + 1 + min) % self.cycle)
                    if posn_id not in visited:
                        insort(
                            to_visit,
                            ((min_to_here + 1 + min, posn_id)),
                            key=lambda x: -1 * x[0],
                        )
        return -2


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    p2 = 0
    blizzards: list[tuple[Point, Direction]] = []
    start, dest = None, None
    char_to_dir = {
        ">": Direction.RIGHT,
        "v": Direction.DOWN,
        "<": Direction.LEFT,
        "^": Direction.UP,
    }
    for row_idx, line in enumerate(input_file.read_text().splitlines()):
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
    grid = Grid(Point(len(line) - 2, row_idx - 1))
    for blizzard_posn, blizzard_dir in blizzards:
        grid.add_blizzard(blizzard_posn, blizzard_dir)
    grid.perf()

    p1 = (
        grid.dj(start, 0, dest) + 1
    )  # Extra 1 to account for getting to the edge from dest
    back_to_start = (
        grid.dj(Point(dest.x, dest.y + 1), p1 % grid.cycle, Point(start.x, start.y + 1))
        + 1
    )  # Extra 1 to account for getting to the edge from dest
    back_to_dest = grid.dj(start, (p1 + back_to_start) % grid.cycle, dest) + 1
    p2 = p1 + back_to_start + back_to_dest
    return (p1, p2)


if __name__ == "__main__":
    utils.per_day_main()
