"""
Advent Of Code 2022 Day 16
"""

from __future__ import annotations


from pathlib import Path
from collections import deque
from typing import NamedTuple
from dataclasses import dataclass, field

import utils


@dataclass
class Valve:
    name: str
    flow_rate: int
    connected_valve_strs: list[str]
    connected_valves: list[Valve] | None = None
    time_to_valve: dict[str, int] | None = None


def max_flow(at_valve: Valve, time_left: int, valves_to_open: set[str], release_rate: int, pressure_released: int) -> int:
    if time_left == 0 or not valves_to_open:
        return pressure_released + release_rate * time_left
    else:
        max_flows = [max_flow(next_valve, time_left - 1, valves_to_open, release_rate, pressure_released + release_rate) for next_valve in at_valve.connected_valves]

        # Now 'visit' opening the valve
        if at_valve.name in valves_to_open:
            valves_to_open = valves_to_open.copy()
            valves_to_open.remove(at_valve.name)
            max_flows.append(max_flow(at_valve, time_left - 1, valves_to_open, release_rate + at_valve, pressure_released + release_rate))
        return max(max_flows)


def compute_times_from_valve(start_valve: Valve) -> None:
    to_visit = deque([(start_valve, 0)])
    visited: dict[str, int] = {}
    while to_visit:
        visiting, path_so_far = to_visit.pop()
        visited[visiting.name] = path_so_far
        for valve in visiting.connected_valves:
            next_path = path_so_far + 1
            if valve.name not in visited:
                to_visit.appendleft((valve, next_path))
    start_valve.time_to_valve = visited


def compute_times(valves: dict[str, Valve]):
    for valve in valves.values():
        compute_times_from_valve(valve)


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    p1, p2 = (0, 0)
    valves: dict[str, Valve] = {}
    for line in input_file.read_text().splitlines():
        tokens = line.split(maxsplit=9)
        valves[tokens[1]] = Valve(tokens[1], int(tokens[4].split("=")[1][:-1]), tokens[9].split(", "))

    for v in valves.values():
        v.connected_valves = [valves[valve_str] for valve_str in v.connected_valve_strs]
    compute_times(valves)

    valves_to_open = set(v.name for v in valves.values() if v.flow_rate > 0)
    to_visit: list[tuple[Valve, int, int, int, set[str]]] = [(valves["AA"], 0, 0, 30, valves_to_open)]
    max_p_release = -1
    visited: set[tuple[str, frozenset]] = set()
    while to_visit:
        visiting, pressure_released, release_rate, time_left, valves_to_open = to_visit.pop()
        fs_to_open = frozenset(valves_to_open)
        visited.add((visiting.name, fs_to_open, time_left, pressure_released))
        if time_left == 0 or not valves_to_open:
            # No more valves to open so no point spinning around wasting time
            max_p_release = max(max_p_release, pressure_released + release_rate * time_left)
        else:
            # Visit neghbours without opening valve
            for next_valve in visiting.connected_valves:
                if (next_valve.name, fs_to_open, time_left - 1, pressure_released + release_rate) not in visited:
                    to_visit.append((next_valve, pressure_released + release_rate, release_rate, time_left - 1, valves_to_open.copy()))

            # Now 'visit' opening the valve
            if visiting.name in valves_to_open:
                valves_to_open.remove(visiting.name)
                if (visiting.name, frozenset(valves_to_open), time_left - 1, pressure_released + release_rate) not in visited:
                    to_visit.append((visiting, pressure_released + release_rate, release_rate + visiting.flow_rate,
                                     time_left - 1, valves_to_open.copy()))
            #to_visit.sort(key=lambda x: x[1] + x[2] * x[3])

    p1 = max_p_release
    return (p1, p2)


if __name__ == "__main__":
    print(p1p2(utils.example_input()))
    print(p1p2(utils.real_input()))
