"""
Advent Of Code 2022 Day 18
"""

from __future__ import annotations


from pathlib import Path
from typing import NamedTuple, Iterator
from collections import defaultdict

import utils


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def adjacents(self) -> Iterator[Point]:
        for offset in (-1, 1):
            yield Point(self.x + offset, self.y, self.z)
        for offset in (-1, 1):
            yield Point(self.x, self.y + offset, self.z)
        for offset in (-1, 1):
            yield Point(self.x, self.y, self.z + offset)


def surface_of_point_cloud(points: set[Point]) -> tuple[int, set[Point]]:
    adjacents: dict[Point, int] = defaultdict(int)
    for p in points:
        for adj in p.adjacents():
            adjacents[adj] += 1

    num_adj = sum(adjacents.get(p, 0) for p in points)
    return len(points) * 6 - num_adj, set(adjacents.keys()) - points


def find_outside(points: set[Point]) -> set[Point]:
    xys: dict[tuple[int, int], tuple[int, int]] = {}
    xzs: dict[tuple[int, int], tuple[int, int]] = {}
    yzs: dict[tuple[int, int], tuple[int, int]] = {}

    for p in points:
        for val, key, store in zip(
            p, ((p.y, p.z), (p.x, p.z), (p.x, p.y)), (yzs, xzs, xys)
        ):
            c_max, c_min = store.get(key, (None, None))
            c_max = val if c_max is None else max(c_max, val)
            c_min = val if c_min is None else min(c_min, val)
            store[key] = (c_max, c_min)

    outside: set[Point] = set()
    for (x, y), (z_max, z_min) in xys.items():
        outside.add(Point(x, y, z_max + 1))
        outside.add(Point(x, y, z_min - 1))
    for (x, z), (y_max, y_min) in xzs.items():
        outside.add(Point(x, y_max + 1, z))
        outside.add(Point(x, y_min - 1, z))
    for (y, z), (x_max, x_min) in yzs.items():
        outside.add(Point(x_max + 1, y, z))
        outside.add(Point(x_min - 1, y, z))
    return outside


def find_inside(points: set[Point], edge: set[Point]) -> set[Point]:
    outside = find_outside(points)

    inside: set[Point] = set()
    poss_inside_points = edge - outside
    while poss_inside_points:
        poss_inside = poss_inside_points.pop()
        can_reach_outside = False
        to_visit: set[Point] = set([poss_inside])
        visited: set[Point] = set()
        while to_visit and not can_reach_outside:
            visiting = to_visit.pop()
            visited.add(visiting)
            for adj in visiting.adjacents():
                if adj not in points:  # Not a droplet
                    if adj in outside:  # We can reach outside so skip this
                        can_reach_outside = True
                        break
                    elif adj not in visited:
                        to_visit.add(adj)
        if not can_reach_outside:
            inside.update(visited)
        poss_inside_points = (
            poss_inside_points - visited
        )  # Either visted are dfinitely in or outside not possible anymore
    return inside


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    droplets = set(
        [
            Point(*map(int, line.split(",")))
            for line in input_file.read_text().splitlines()
        ]
    )

    p1, edge = surface_of_point_cloud(droplets)
    inner_area, _ = surface_of_point_cloud(find_inside(droplets, edge))

    return (p1, p1 - inner_area)


if __name__ == "__main__":
    print(p1p2(utils.example_input()))
    print(p1p2(utils.real_input()))
