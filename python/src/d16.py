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


def max_flow(
    at_valve: Valve,
    time_left: int,
    valves_to_open: set[str],
    release_rate: int,
    valves: dict[str, Valve],
) -> int:
    max_flows = [release_rate * time_left]  # Do nothing flow

    valve_open_times = [
        (valves[v_str], at_valve.time_to_valve[v_str] + 1)
        for v_str in valves_to_open
        if at_valve.time_to_valve[v_str] + 1 <= time_left
    ]
    for valve_to_open, time_to_open in valve_open_times:
        next_valves_to_open = valves_to_open.copy()
        next_valves_to_open.remove(valve_to_open.name)
        max_flows.append(
            time_to_open * release_rate
            + max_flow(
                valve_to_open,
                time_left - time_to_open,
                next_valves_to_open,
                release_rate + valve_to_open.flow_rate,
                valves,
            )
        )

    return max(max_flows)


def max_flow_two(
    at_valve: Valve,
    e_at_valve: Valve,
    time_left: int,
    valves_to_open: set[str],
    release_rate: int,
    valves: dict[str, Valve],
) -> int:
    max_flows = [release_rate * time_left]  # Do nothing flow

    valve_open_times = [
        (valves[v_str], at_valve.time_to_valve[v_str] + 1)
        for v_str in valves_to_open
        if at_valve.time_to_valve[v_str] + 1 <= time_left
    ]
    for valve_to_open, time_to_open in valve_open_times:
        next_valves_to_open = valves_to_open.copy()
        next_valves_to_open.remove(valve_to_open.name)
        max_flows.append(
            time_to_open * release_rate
            + max_flow(
                valve_to_open,
                time_left - time_to_open,
                next_valves_to_open,
                release_rate + valve_to_open.flow_rate,
                valves,
            )
        )

    return max(max_flows)


def shortest_paths(start_valve: Valve) -> None:
    to_visit = deque([(start_valve, 0)])
    visited: dict[str, int] = {}
    while to_visit:
        visiting, path_so_far = to_visit.pop()
        if visiting.name not in visited:
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
        valves[tokens[1]] = Valve(
            tokens[1], int(tokens[4].split("=")[1][:-1]), tokens[9].split(", ")
        )

    for v in valves.values():
        v.connected_valves = [valves[valve_str] for valve_str in v.connected_valve_strs]

    for valve in valves.values():
        shortest_paths(valve)

    valves_to_open = set(v.name for v in valves.values() if v.flow_rate > 0)
    p1 = max_flow(valves["AA"], 30, valves_to_open, 0, valves)
    # p2 = max_flow_two(valves["AA"], valves["AA"], 26, valves_to_open, 0, valves)
    return (p1, p2)


if __name__ == "__main__":
    print(p1p2(utils.example_input()))
    print(p1p2(utils.real_input()))
