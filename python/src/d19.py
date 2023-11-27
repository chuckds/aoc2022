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


class ResCounts(NamedTuple):
    ore: int = 0
    cla: int = 0
    obs: int = 0
    geo: int = 0

    def better_than(self, other: ResCounts) -> bool:
        return all(s_r == -1 or s_r >= o_r >= 0 for s_r, o_r in zip(self, other))

    def worse_than(self, other: ResCounts) -> bool:
        return all(o_r == -1 or o_r >= s_r >= 0 for s_r, o_r in zip(self, other))

def min_to_afford(cost: ResCounts, bank: ResCounts, robots: ResCounts) -> int:
    # Cope with bank of -1 representing "enough"
    shortfall = [(c - b) if c > b >= 0 else 0 for b, c in zip(bank, cost)]
    if any(s > 0 and r == 0 for s, r in zip(shortfall, robots)):
        # Have a shortfall in a resource for which there is no robot so it won't
        # be affordable
        return sys.maxsize
    return max(
        math.ceil(s / r) if r > 0 else 0 for s, r in zip(shortfall, robots)
    )


def calc_new_bank(
    num_days: int,
    bank: ResCounts,
    robot_counts: ResCounts,
    cost: ResCounts = ResCounts(),
) -> ResCounts:
    # Preseve a resource being -1 if it already is
    return ResCounts(
        *((b + (r * num_days) - c) if b >= 0 else -1 for b, r, c in zip(bank, robot_counts, cost))
    )


def state_geode_every_min(bp: Blueprint, bank: ResCounts, robot_counts: ResCounts) -> bool:
    return all(r >= c and (b == -1 or b >= c) for r, b, c in zip(robot_counts, bank, bp.res_robot_costs[3]))


class FactoryState(NamedTuple):
    time_left: int
    bank: ResCounts
    robot_counts: ResCounts

    def can_build_a_geo_a_min(self) -> bool:
        return self.robot_counts[0] < 0

    def better_than(self, other: FactoryState) -> bool:
        if self.can_build_a_geo_a_min():
            # Could do some maths here
            return self.bank.geo > other.bank.geo and self.robot_counts.geo > other.robot_counts.geo
        else:
            return self.bank.better_than(other.bank) and self.robot_counts.better_than(other.robot_counts)

    def worse_than(self, other: FactoryState) -> bool:
        if other.can_build_a_geo_a_min():
            # Could do some maths here
            return self.bank.geo < other.bank.geo and self.robot_counts.geo < other.robot_counts.geo
        else:
            return self.bank.worse_than(other.bank) and self.robot_counts.worse_than(other.robot_counts)

    def child_states(self, bp: Blueprint) -> list[FactoryState]:
        new_states = []
        have_bought_nothing = False
        for res_idx, robot_cost in bp.res_robot_costs.items():
            if self.bank[res_idx] < 0:
                # We have enough robots of this type to afford any robot every
                # minute no need to build any more (doesn't apply to geodes)
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
                    **{ResCounts._fields[res_idx]: self.robot_counts[res_idx] + 1}
                )
                if (res_idx != 3 and new_bank[res_idx] >= 0
                    and bp.max_robot_res_cost[res_idx] <= new_robot_counts[res_idx]
                    and bp.max_robot_res_cost[res_idx] <= new_bank[res_idx]):
                    # The new state has enough robots of this resource to be
                    # able to build any resource robot every minute.
                    # In addition it has enough in the bank as well.
                    # This means it no longer matters how much it has in
                    # the bank for this resource
                    new_bank = new_bank._replace(
                        **{ResCounts._fields[res_idx]: -1}
                    )
                if state_geode_every_min(bp, new_bank, new_robot_counts):
                    # Set everything but #geo robots and #geo bank to -1
                    new_bank = ResCounts(-1, -1, -1, new_bank.geo)
                    new_robot_counts = ResCounts(-1, -1, -1, new_robot_counts.geo)
                new_states.append(
                    FactoryState(
                        self.time_left - min_to_earn - 1, new_bank, new_robot_counts
                    )
                )
            elif not have_bought_nothing:
                have_bought_nothing = True
                # Not enough time to build so don't do anything
                buy_nothing_bank = calc_new_bank(self.time_left, self.bank, self.robot_counts)
                new_states.append(FactoryState(0, buy_nothing_bank, self.robot_counts))
        return new_states


@dataclass
class Blueprint:
    num: int
    res_robot_costs: dict[int, ResCounts]

    @functools.cached_property
    def max_robot_res_cost(self) -> ResCounts:
        """Get the max cost of each resource type across all robot types."""
        max_res = []
        for idx in range(len(ResCounts._fields)):
            max_res.append(
                max(robot_cost[idx] for robot_cost in self.res_robot_costs.values())
            )
        return ResCounts(*max_res)

    def max_geodes(self, time_available: int) -> int:
        time_to_states = {time_available: {FactoryState(time_available, ResCounts(), ResCounts(1))}}
        best_state_seen = FactoryState(time_available, ResCounts(), ResCounts())
        states_checked = 0
        trimmed = 0
        for time in range(time_available, 0, -1):
            states_to_check = time_to_states.get(time, set())
            for state_to_check in states_to_check:
                states_checked += 1
                if state_to_check.better_than(best_state_seen):
                    best_state_seen = state_to_check
                elif state_to_check.worse_than(best_state_seen):
                    trimmed += 1
                    continue
                for new_state in state_to_check.child_states(self):
                    time_to_states.setdefault(new_state.time_left, set()).add(
                        new_state
                    )
            if states_to_check:
                del time_to_states[time]
                print(
                    f"{time} min left, {len(states_to_check):,} states checked ({trimmed=:,})"
                )
        max_state = max(time_to_states[0], key=lambda state: state.bank.geo)
        print(
            f"bp: {self.num} {max_state.bank.geo=} states checked: {states_checked} {max_state} "
        )
        return max_state.bank.geo

    @classmethod
    def from_line(cls, line: str) -> Blueprint:
        bp, costs = line.split(":")
        bp_num = int(bp.split()[1])
        return cls(bp_num, get_bp_robot_costs(costs))


def get_bp_robot_costs(costs: str) -> dict[int, ResCounts]:
    robot_costs = {}
    for robot_info_line in costs.split(".")[:-1]:
        _, robot_name, _, _, cost_info = robot_info_line.split(maxsplit=4)
        robot_cost = ResCounts()
        for cost_part in cost_info.split(" and "):
            num_str, res_str = cost_part.split()
            robot_cost = robot_cost._replace(**{res_str[:3]: int(num_str)})
        robot_costs[ResCounts._fields.index(robot_name[:3])] = robot_cost
    return robot_costs


def p1(input_file: Path = utils.real_input()) -> int:
    bps = [
        Blueprint.from_line(line) for line in input_file.read_text().splitlines()
    ]
    return sum(bp.num * bp.max_geodes(24) for bp in bps)


def p2(input_file: Path = utils.real_input()) -> int:
    bps = [
        Blueprint.from_line(line) for line in input_file.read_text().splitlines()
    ]
    return math.prod(bp.max_geodes(32) for bp in bps[:3])


if __name__ == "__main__":
    utils.per_day_main()
