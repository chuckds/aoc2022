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


class DetectionEdgeLine(NamedTuple):
    y_intercept: int
    no_beacons_below: bool
    slope_down: bool


def p2(sensor_beacons: list[tuple[Point, Point, int]]) -> int:
    """
    If there is only one point where the beacon can be then it must be just
    on the edge of the detection zone of 4 sesors.
    Note: This ignores the x and y limits provided by the problem...
    """

    # For each sensor compute the y intercept of each of the 4 lines that
    # define the boundary *just* outside its detection zone
    edge_pairs: dict[bool, set[int]] = {}
    detection_edges: dict[DetectionEdgeLine, list[tuple[Point, int]]] = {}
    for sensor, _, detection_size in sensor_beacons:
        for no_beacons_below in (False, True):
            for slope_down in (False, True):
                if no_beacons_below:
                    point_on_edge_y = sensor.y - (detection_size + 1)
                else:
                    point_on_edge_y = sensor.y + (detection_size + 1)
                if slope_down:
                    y_intercept = point_on_edge_y - sensor.x
                else:
                    y_intercept = point_on_edge_y + sensor.x
                this_edge = DetectionEdgeLine(y_intercept, no_beacons_below, slope_down)
                detection_edges.setdefault(this_edge, []).append(
                    (sensor, detection_size)
                )

                if (
                    DetectionEdgeLine(y_intercept, not no_beacons_below, slope_down)
                    in detection_edges
                ):
                    # The opposite partner of this edge is present - which means's there is a line where
                    # beacons could be with areas where they can't above and below
                    edge_pairs.setdefault(slope_down, set()).add(y_intercept)

    # For each pair of lines (one sloping down and one up) compute the intersection point
    # This point *might be* on the edge of 4 sensor detection zones.
    candidate_points: set[Point] = set()
    for slope_down_intercept in edge_pairs.get(True, set()):
        for slope_up_intercept in edge_pairs.get(False, set()):
            intersec = Point(
                (slope_up_intercept - slope_down_intercept) // 2,
                (slope_up_intercept + slope_down_intercept) // 2,
            )

            # Check that this intersection point is on the edge of each of the 4 sensor locations
            # So far nothing is bounding the lines of the detection zone boarder
            # and so the point could be too far away from the sensor zone
            on_edges = True
            for no_beacons_below in (False, True):
                for slope_down in (False, True):
                    y_intercept = (
                        slope_down_intercept if slope_down else slope_up_intercept
                    )
                    on_an_edge = False
                    for sensor, detection_size in detection_edges[
                        DetectionEdgeLine(y_intercept, no_beacons_below, slope_down)
                    ]:
                        if no_beacons_below:
                            y_ok = (
                                (sensor.y - (detection_size + 1))
                                <= intersec.y
                                <= sensor.y
                            )
                        else:
                            y_ok = (
                                sensor.y
                                <= intersec.y
                                <= sensor.y + (detection_size + 1)
                            )
                        if no_beacons_below == slope_down:
                            x_ok = (
                                sensor.x
                                <= intersec.x
                                <= sensor.x + (detection_size + 1)
                            )
                        else:
                            x_ok = (
                                (sensor.x - (detection_size + 1))
                                <= intersec.x
                                <= sensor.x
                            )
                        on_an_edge = on_an_edge or (x_ok and y_ok)
                    on_edges = on_edges and on_an_edge
            if on_edges:
                candidate_points.add(intersec)

    # After all this, it is possible that these points just on the edge of 4 detection zones
    # might be int he middle of one or more detection zones - making them useless
    for candidate in candidate_points:
        for sensor, _, detection_size in sensor_beacons:
            if candidate.taxicab_dist(sensor) <= detection_size:
                break
        else:
            # This point isn't within another sensor's detection zone
            result = candidate
            break

    return result.x * 4_000_000 + result.y


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
