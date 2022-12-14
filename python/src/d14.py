"""
Advent Of Code 2022 d14
"""

from __future__ import annotations


from pathlib import Path
from typing import NamedTuple, Iterator

import utils


class Point(NamedTuple):
    x: int
    y: int

    def next_sand_posn(self) -> Iterator[Point]:
        for x_delt in (0, -1, 1):
            yield Point(self.x + x_delt, self.y + 1)


class Line(NamedTuple):
    st: Point
    end: Point

    def __iter__(self) -> Iterator[Point]:
        xdir = 1 if self.end.x >= self.st.x else - 1
        ydir = 1 if self.end.y >= self.st.y else - 1
        for x in range(self.st.x, self.end.x + xdir, xdir):
            for y in range(self.st.y, self.end.y + ydir, ydir):
                yield Point(x, y)


SAND_POINT = Point(500, 0)


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    p1, p2 = (0, 0)
    blocked: set[Point] = set()
    max_rock_y = 0
    for line in input_file.read_text().splitlines():
        points = line.split(" -> ")
        st = Point(*map(int, points[0].split(",")))
        max_rock_y = max(max_rock_y, st.y)
        for p in points[1:]:
            end = Point(*map(int, p.split(",")))
            max_rock_y = max(max_rock_y, end.y)
            blocked.update(Line(st, end))
            st = end

    floor = max_rock_y + 2
    sand_units = 1
    sand_pos = SAND_POINT
    while True:
        for next_sand in sand_pos.next_sand_posn():
            if next_sand.y < floor and next_sand not in blocked:
                sand_pos = next_sand
                break
        else:  # No break
            if sand_pos == SAND_POINT:
                break
            blocked.add(sand_pos)
            sand_units += 1
            sand_pos = SAND_POINT

        if p1 == 0 and sand_pos.y >= max_rock_y:  # Sand has fallen past last rocks
            p1 = sand_units - 1

    return (p1, sand_units)


if __name__ == "__main__":
    print(p1p2(utils.example_input()))
    print(p1p2(utils.real_input()))
