"""
Advent Of Code 2022 Day 19
"""

from __future__ import annotations


from enum import Enum
from pathlib import Path
from typing import NamedTuple
from dataclasses import dataclass
from bisect import insort, bisect_right, bisect_left
import math
import sys

import utils


class Resource(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


class PerResCounts(NamedTuple):
    ore: int
    cly: int
    obs: int
    geo: int


PER_RES_COUNT = list[int]
ROBOT_COSTS = list[PER_RES_COUNT]


def can_afford(cost: PER_RES_COUNT, bank: PER_RES_COUNT) -> int:
    return all(b >= c for b, c in zip(bank, cost))


def how_many_can_afford(cost: PER_RES_COUNT, bank: PER_RES_COUNT) -> int:
    how_many = [b // c for b, c in zip(bank, cost) if c > 0]
    return min(how_many)


def min_to_afford(
    cost: PER_RES_COUNT, bank: PER_RES_COUNT, robots: PER_RES_COUNT
) -> int:
    shortfall = [c - b for b, c in zip(bank, cost)]
    if any(s > 0 and r == 0 for s, r in zip(shortfall, robots)):
        # Have a shortfall in a resource for which there is no robot so it won't
        # be affordable
        return sys.maxsize
    return max(
        math.ceil(s / r) if s > 0 else 0 for s, r in zip(shortfall, robots) if r > 0
    )


FREE = [0] * len(Resource)


def calc_new_bank(num_days: int, bank: PER_RES_COUNT, robot_counts: PER_RES_COUNT, cost: PER_RES_COUNT = FREE) -> PER_RES_COUNT:
    return [b + (r * num_days) - c for b, r, c in zip(bank, robot_counts, cost)]


def recurse(bp: Blueprint, time_left: int, bank: PER_RES_COUNT, robot_counts: PER_RES_COUNT) -> int:
    buy_nothing_bank = calc_new_bank(time_left, bank, robot_counts)
    mgs = [buy_nothing_bank[Resource.GEODE.value]]
    for res in Resource:
        robot_cost = bp.res_robot_costs[res.value]
        min_to_earn = min_to_afford(robot_cost, bank, robot_counts)
        if min_to_earn < time_left:
            # There is enough time to wait until this robot can be afforded so
            # try that
            # Add a minute while the robot is constructed
            new_bank = calc_new_bank(min_to_earn + 1, bank, robot_counts, robot_cost)
            new_robot_counts = robot_counts[:]
            new_robot_counts[res.value] += 1
            mgs.append(recurse(bp, time_left - min_to_earn - 1, new_bank, new_robot_counts))
    return max(mgs)


class FactoryState(NamedTuple):
    time_left: int
    bank: PER_RES_COUNT
    robot_counts: PER_RES_COUNT


def non_recurse(bp: Blueprint, time_left: int, bank: PER_RES_COUNT, robot_counts: PER_RES_COUNT) -> int:
    states_to_check = [FactoryState(time_left, bank, robot_counts)]
    states_checked = set()
    buy_nothing_bank = calc_new_bank(time_left, bank, robot_counts)
    mgs = [buy_nothing_bank[Resource.GEODE.value]]
    for res in Resource:
        robot_cost = bp.res_robot_costs[res.value]
        min_to_earn = min_to_afford(robot_cost, bank, robot_counts)
        if min_to_earn < time_left:
            # There is enough time to wait until this robot can be afforded so
            # try that
            # Add a minute while the robot is constructed
            new_bank = calc_new_bank(min_to_earn + 1, bank, robot_counts, robot_cost)
            new_robot_counts = robot_counts[:]
            new_robot_counts[res.value] += 1
            mgs.append(recurse(bp, time_left - min_to_earn - 1, new_bank, new_robot_counts))
    return max(mgs)


@dataclass
class Blueprint:
    num: int
    res_robot_costs: ROBOT_COSTS

    def max_geodes(self, time_available: int) -> int:
        robot_counts = [0] * len(Resource)
        robot_counts[Resource.ORE.value] = 1
        return recurse(self, time_available, [0] * len(Resource), robot_counts)


def get_bp_costs(costs: str) -> ROBOT_COSTS:
    robot_costs = [[0] * len(Resource) for _ in range(len(Resource))]
    for robot_info_line in costs.split(".")[:-1]:
        _, robot, _, _, cost_info = robot_info_line.split(maxsplit=4)
        robot_cost = robot_costs[Resource[robot.upper()].value]
        for cost_part in cost_info.split(" and "):
            num_str, res_str = cost_part.split()
            robot_cost[Resource[res_str.upper()].value] = int(num_str)
    return robot_costs


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    blueprints: list[Blueprint] = []
    p1, p2 = (0, 0)
    for blueprint_line in input_file.read_text().splitlines():
        bp, costs = blueprint_line.split(":")
        bp_num = int(bp.split()[1])
        robot_info = get_bp_costs(costs)
        blueprints.append(Blueprint(bp_num, robot_info))

    time_available = 24
    quality_levels = [blueprint.num * blueprint.max_geodes(time_available) for blueprint in blueprints]
    p1 = sum(quality_levels)

    return (p1, p2)


if __name__ == "__main__":
    utils.per_day_main()
