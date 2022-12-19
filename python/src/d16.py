"""
Advent Of Code 2022 Day 16
"""

from __future__ import annotations


from pathlib import Path
from collections import deque
from dataclasses import dataclass, field

import utils


@dataclass
class Valve:
    name: str
    flow_rate: int
    connected_valve_strs: list[str]
    connected_valves: list[Valve] = field(default_factory=list)
    time_to_valve: dict[str, int] = field(default_factory=dict)


def max_flow(at_valve: Valve, time_left: int, valves_to_open: set[str], release_rate: int, pressure_released: int, valves: dict[str, Valve]) -> int:
    times = [(v_str, at_valve.time_to_valve[v_str] + 1)
             for v_str in valves_to_open
             if at_valve.time_to_valve[v_str] + 1 <= time_left]
    if not times:
        return pressure_released + release_rate * time_left
    else:
        max_flows = []
        for valve_to_open_str, time_to_get_there in times:
            valve_to_open = valves[valve_to_open_str]
            next_valves_to_open = valves_to_open.copy()
            next_valves_to_open.remove(valve_to_open_str)
            max_flows.append(max_flow(valve_to_open, time_left - time_to_get_there, next_valves_to_open,
                                      release_rate + valve_to_open.flow_rate, pressure_released + time_to_get_there * release_rate, valves))
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


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    p1, p2 = (0, 0)
    valves: dict[str, Valve] = {}
    for line in input_file.read_text().splitlines():
        tokens = line.split(maxsplit=9)
        valves[tokens[1]] = Valve(tokens[1], int(tokens[4].split("=")[1][:-1]), tokens[9].split(", "))

    for v in valves.values():
        v.connected_valves = [valves[valve_str] for valve_str in v.connected_valve_strs]

    for valve in valves.values():
        compute_times_from_valve(valve)

    p1 = max_flow(valves["AA"], 30, set(v.name for v in valves.values() if v.flow_rate), 0, 0, valves)
    return (p1, p2)


if __name__ == "__main__":
    print(p1p2(utils.example_input()))
    print(p1p2(utils.real_input()))
