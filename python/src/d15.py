"""
Advent Of Code 2022 Day 15
"""

from __future__ import annotations


import re
from pathlib import Path
from typing import NamedTuple

import utils


input_line_re = re.compile(
    r"[^=]*=(?P<sensx>-?[0-9]+)[^=]*=(?P<sensy>-?[0-9]+)[^=]*=(?P<beacx>-?[0-9]+)[^=]*=(?P<beacy>-?[0-9]+)"
)


class Point(NamedTuple):
    x: int
    y: int

    def taxicab_dist(self, other: Point) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


def len_ranges(ranges: list[range]) -> int:
    counted_upto = -1_000_000_000
    res = 0
    for r in sorted(ranges, key=lambda x: x.start):
        res += max(counted_upto, r.stop) - max(counted_upto, r.start)
        counted_upto = max(counted_upto, r.stop)
    return res


def p1(sensor_beacons: list[tuple[Point, Point, int]]) -> int:
    target_row = 10 if len(sensor_beacons) < 15 else 2_000_000

    range_block_on_target: list[range] = []
    beacons_on_target_row: set[Point] = set()
    for sensor, beacon, detection_size in sensor_beacons:
        if beacon.y == target_row:
            beacons_on_target_row.add(beacon)
        sensor_pen = detection_size - abs(sensor.y - target_row)
        if sensor_pen >= 0:
            range_block_on_target.append(
                range(sensor.x - sensor_pen, sensor.x + sensor_pen + 1)
            )

    return len_ranges(range_block_on_target) - len(beacons_on_target_row)


def p2(sensor_beacons: list[tuple[Point, Point, int]]) -> int:
    dim_max = 20 if len(sensor_beacons) < 15 else 4_000_000

    row_ranges: dict[int, list[range]] = {}
    for sensor, _, detection_size in sensor_beacons:
        if sensor.x + detection_size >= 0 and sensor.x - detection_size <= dim_max:
            for row in range(
                max(0, sensor.y - detection_size),
                min(dim_max, sensor.y + detection_size) + 1,
            ):
                sensor_pen = detection_size - abs(sensor.y - row)
                row_ranges.setdefault(row, []).append(
                    range(sensor.x - sensor_pen, sensor.x + sensor_pen + 1)
                )

    x_val = -10
    for row, blocked_ranges in row_ranges.items():
        counted_upto = 0
        for r in sorted(blocked_ranges, key=lambda x: x.start):
            range_from = max(counted_upto, r.start)
            if range_from > counted_upto:
                # Break in the range
                x_val = counted_upto
                break
            counted_upto = max(counted_upto, r.stop)
            if counted_upto > dim_max:
                break
        if x_val >= 0:
            return x_val * 4_000_000 + row

    return 0


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    sensor_beacons: list[tuple[Point, Point, int]] = []
    for line in input_file.read_text().splitlines():
        m = input_line_re.match(line)
        if m:
            sensor = Point(int(m.group("sensx")), int(m.group("sensy")))
            beacon = Point(int(m.group("beacx")), int(m.group("beacy")))
            sensor_beacons.append((sensor, beacon, sensor.taxicab_dist(beacon)))

    return (p1(sensor_beacons), p2(sensor_beacons))


if __name__ == "__main__":
    print(p1p2(utils.example_input()))
    print(p1p2(utils.real_input()))
