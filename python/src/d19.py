"""
Advent Of Code 2022 Day 19
"""

from __future__ import annotations


import functools
from pathlib import Path
from typing import NamedTuple
from dataclasses import dataclass
import math
import sys

import utils


class PerResCounts(NamedTuple):
    ore: int = 0
    cla: int = 0
    obs: int = 0
    geo: int = 0


def min_to_afford(cost: PerResCounts, bank: PerResCounts, robots: PerResCounts) -> int:
    shortfall = [c - b for b, c in zip(bank, cost)]
    if any(s > 0 and r == 0 for s, r in zip(shortfall, robots)):
        # Have a shortfall in a resource for which there is no robot so it won't
        # be affordable
        return sys.maxsize
    return max(
        math.ceil(s / r) if s > 0 else 0 for s, r in zip(shortfall, robots) if r > 0
    )


def calc_new_bank(
    num_days: int,
    bank: PerResCounts,
    robot_counts: PerResCounts,
    cost: PerResCounts = PerResCounts(),
) -> PerResCounts:
    return PerResCounts(
        *(b + (r * num_days) - c for b, r, c in zip(bank, robot_counts, cost))
    )


@dataclass
class RecurseContext:
    max_level: int = 0
    num_calls: int = 0


def recurse(
    bp: Blueprint,
    time_left: int,
    bank: PerResCounts,
    robot_counts: PerResCounts,
    ctx: RecurseContext,
    lvl: int = 0,
) -> int:
    ctx.num_calls += 1
    ctx.max_level = max(lvl, ctx.max_level)
    buy_nothing_bank = calc_new_bank(time_left, bank, robot_counts)
    mgs = [buy_nothing_bank.geo]
    for res_name, robot_cost in bp.res_robot_costs.items():
        min_to_earn = min_to_afford(robot_cost, bank, robot_counts)
        if min_to_earn + 1 < time_left:
            # Only explore this option if there is enough time to
            # - wait for the funds needed to build the robot
            # - build the robot
            # - some time left to earn resource from the robot
            new_bank = calc_new_bank(min_to_earn + 1, bank, robot_counts, robot_cost)
            new_robot_counts = robot_counts._replace(
                **{res_name: getattr(robot_counts, res_name) + 1}
            )
            mgs.append(
                recurse(
                    bp,
                    time_left - min_to_earn - 1,
                    new_bank,
                    new_robot_counts,
                    ctx,
                    lvl + 1,
                )
            )
    return max(mgs)


class FactoryState(NamedTuple):
    time_left: int
    bank: PerResCounts
    robot_counts: PerResCounts

    def child_states(self, bp: Blueprint) -> list[FactoryState]:
        buy_nothing_bank = calc_new_bank(
            self.time_left, self.bank, self.robot_counts
        )
        new_states = [FactoryState(0, buy_nothing_bank, self.robot_counts)]
        for res_name, robot_cost in bp.res_robot_costs.items():
            if res_name != "geo" and getattr(bp.max_robot_res_cost, res_name) <= getattr(self.robot_counts, res_name):
                # We have enough robots to afford any robot every minute
                # no need to build any more
                continue
            min_to_earn = min_to_afford(robot_cost, self.bank, self.robot_counts)
            if min_to_earn + 1 < self.time_left:
                # Only explore this option if there is enough time to
                # - wait for the funds needed to build the robot
                # - build the robot
                # - some time left to earn resource from the robot
                new_bank = calc_new_bank(
                    min_to_earn + 1, self.bank, self.robot_counts, robot_cost
                )
                new_robot_counts = self.robot_counts._replace(
                    **{res_name: getattr(self.robot_counts, res_name) + 1}
                )
                new_state = FactoryState(
                    self.time_left - min_to_earn - 1, new_bank, new_robot_counts
                )
                new_states.append(new_state)
        return new_states


def get_bp_robot_costs(costs: str) -> dict[str, PerResCounts]:
    robot_costs = {}
    for robot_info_line in costs.split(".")[:-1]:
        _, robot_name, _, _, cost_info = robot_info_line.split(maxsplit=4)
        robot_cost = PerResCounts()
        for cost_part in cost_info.split(" and "):
            num_str, res_str = cost_part.split()
            robot_cost = robot_cost._replace(**{res_str[:3]: int(num_str)})
        robot_costs[robot_name[:3]] = robot_cost
    return robot_costs


@dataclass
class Blueprint:
    num: int
    res_robot_costs: dict[str, PerResCounts]

    @functools.cached_property
    def max_robot_res_cost(self) -> PerResCounts:
        """Get the max cost of each resource type across all robot types."""
        max_res = []
        for res_name in PerResCounts._fields:
            max_res.append(max(getattr(robot_cost, res_name) for robot_cost in self.res_robot_costs.values()))
        return PerResCounts(*max_res)

    def max_geodes(self, time_available: int) -> int:
        ctx = RecurseContext()
        answer = recurse(
            self,
            time_available,
            PerResCounts(),
            PerResCounts(1),
            ctx,
        )
        print(f"bp: {self.num}, max_geo: {answer} ctx: {ctx}")
        return answer

    def max_geodes2(self, time_available: int) -> int:
        states_to_check = [
            FactoryState(time_available, PerResCounts(), PerResCounts(1))
        ]
        states_checked = set()
        max_geo = 0
        while states_to_check:
            state_to_check = states_to_check.pop()
            if state_to_check in states_checked:
                continue
            states_checked.add(state_to_check)
            if state_to_check.time_left == 0:
                max_geo = max(state_to_check.bank.geo, max_geo)
            else:
                for new_state in state_to_check.child_states(self):
                    if new_state not in states_checked:
                        states_to_check.append(new_state)

        print(f"bp: {self.num} {max_geo=} states checked: {len(states_checked)}")

        return max_geo

    @classmethod
    def from_line(cls, line: str) -> Blueprint:
        bp, costs = line.split(":")
        bp_num = int(bp.split()[1])
        return cls(bp_num, get_bp_robot_costs(costs))


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    blueprints = [
        Blueprint.from_line(line) for line in input_file.read_text().splitlines()
    ]

    quality_levels = [
        blueprint.num * blueprint.max_geodes2(24) for blueprint in blueprints
    ]
    p1 = sum(quality_levels)
    p2_max_geodes = []
    #p2_max_geodes = [blueprint.max_geodes2(32) for blueprint in blueprints[:3]]
    return (p1, math.prod(p2_max_geodes))


if __name__ == "__main__":
    utils.per_day_main()
