"""
Advent Of Code 2022 Day 12
"""

from __future__ import annotations


import heapq

from functools import total_ordering
from typing import Iterator, Callable
from pathlib import Path
from dataclasses import dataclass

import utils


@total_ordering
@dataclass
class GridLocation:
    row: int
    col: int
    elevation: str
    shortest_path_here: int = -1

    def neighbours(self, grid: list[list[GridLocation]]) -> Iterator[GridLocation]:
        for row_delt in (-1, 0, 1):
            for col_delt in ((-1, 1), (0,))[row_delt]:
                if 0 <= (self.row + row_delt) < len(grid) and 0 <= (
                    self.col + col_delt
                ) < len(grid[0]):
                    yield grid[self.row + row_delt][self.col + col_delt]

    def __lt__(self, other: GridLocation) -> bool:
        return self.shortest_path_here < other.shortest_path_here


PassableCheck = Callable[[GridLocation, GridLocation], bool]


def shortest_route_from(
    from_loc: GridLocation,
    dest_loc: GridLocation | None,
    grid: list[list[GridLocation]],
    passable: PassableCheck,
) -> int:
    result = 0
    known_shortest: list[GridLocation] = []
    from_loc.shortest_path_here = 0
    heapq.heappush(known_shortest, from_loc)
    while known_shortest and result == 0:
        from_loc = heapq.heappop(known_shortest)
        shortest_path = from_loc.shortest_path_here + 1
        for to_loc in from_loc.neighbours(grid):
            if passable(from_loc, to_loc) and to_loc.shortest_path_here == -1:
                to_loc.shortest_path_here = shortest_path
                if to_loc == dest_loc:
                    # We're here!
                    result = dest_loc.shortest_path_here
                    break
                heapq.heappush(known_shortest, to_loc)

    return result


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    rows = []
    destination = None
    for row_idx, line in enumerate(input_file.read_text().splitlines()):
        locations = []
        for col_idx, char in enumerate(line):
            loc = GridLocation(row_idx, col_idx, char)
            if char == "S":
                p1_start = loc
                loc.elevation = "a"
            elif char == "E":
                loc.elevation = "z"
                destination = loc
            locations.append(loc)
        rows.append(locations)

    assert destination is not None

    def passable(from_loc: GridLocation, to_loc: GridLocation) -> bool:
        return ord(from_loc.elevation) + 1 >= ord(to_loc.elevation)

    p1 = shortest_route_from(p1_start, destination, rows, passable)
    for row in rows:
        for loc in row:
            loc.shortest_path_here = -1

    def backwards(from_loc: GridLocation, to_loc: GridLocation) -> bool:
        return ord(from_loc.elevation) - 1 <= ord(to_loc.elevation)

    shortest_route_from(destination, None, rows, backwards)

    p2 = min(
        loc.shortest_path_here
        for row in rows
        for loc in row
        if loc.elevation == "a" and loc.shortest_path_here >= 0
    )
    return (p1, p2)


if __name__ == "__main__":
    print(p1p2(utils.example_input()))
    print(p1p2(utils.real_input()))
