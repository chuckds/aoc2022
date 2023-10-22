"""
Advent Of Code 2022 Day 19
"""

from __future__ import annotations


from enum import Enum
from pathlib import Path
from typing import Iterator
from dataclasses import dataclass
from collections import deque
import math
import sys

import utils


class Resource(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


PER_RES_COUNT = list[int]
ROBOT_COSTS = list[PER_RES_COUNT]


def can_afford(cost: PER_RES_COUNT, bank: PER_RES_COUNT) -> int:
    return all(b >= c for b, c in zip(bank, cost))


def how_many_can_afford(cost: PER_RES_COUNT, bank: PER_RES_COUNT) -> int:
    how_many = [b // c for b, c in zip(bank, cost) if c > 0]
    return min(how_many)


def get_min_to_afford(
    cost: PER_RES_COUNT, bank: PER_RES_COUNT, robots: PER_RES_COUNT
) -> int:
    shortfall = [c - b for b, c in zip(bank, cost)]
    if any(s > 0 and r == 0 for s, r in zip(shortfall, robots)):
        # Never gonna happen
        return sys.maxsize
    return max(
        math.ceil(s / r) if s > 0 else 0 for s, r in zip(shortfall, robots) if r > 0
    )


def algo(
    time_left: int, bank: PER_RES_COUNT, robots: PER_RES_COUNT, bp: Blueprint
) -> Resource | None:
    if time_left <= 1:
        # No point buying anything it won't make a difference
        return None
    better_res_costs: list[tuple[Resource, int]] = []
    for res in (Resource.GEODE, Resource.OBSIDIAN, Resource.CLAY, Resource.ORE):
        res_cost = bp.res_robot_costs[res.value]
        if can_afford(res_cost, bank):
            if better_res_costs:
                # If we bought this what would the bank next min be
                new_bank = [b + i - c for b, c, i in zip(bank, res_cost, robots)]
                new_robots = robots[:]
                new_robots[res.value] += 1
                # Would that delay getting a better robot
                buy = True
                for better_res, better_min_to_afford in better_res_costs:
                    better_res_cost = bp.res_robot_costs[better_res.value]
                    new_min_to_afford = get_min_to_afford(
                        better_res_cost, new_bank, new_robots
                    )
                    if new_min_to_afford + 1 > better_min_to_afford:
                        buy = False
                if buy:
                    return res
            else:
                # Just buy it
                return res
        elif res != Resource.ORE:
            min_to_afford = get_min_to_afford(res_cost, bank, robots)
            if min_to_afford <= time_left:
                # Can afford in time so need to ensure we don't make it later!
                better_res_costs.append((res, min_to_afford))
    return None


@dataclass
class Blueprint:
    num: int
    res_robot_costs: ROBOT_COSTS

    def purchase_options(
        self, bank: PER_RES_COUNT, for_res: Resource = Resource.GEODE
    ) -> Iterator[tuple[PER_RES_COUNT, PER_RES_COUNT]]:
        if for_res == Resource.ORE:
            robot_cost = self.res_robot_costs[for_res.value]
            count = how_many_can_afford(robot_cost, bank)
            for num in range(0, count + 1):
                num_robot_cost = [num * c for c in robot_cost]
                po = [0] * len(Resource)
                po[for_res.value] += num
                yield po, num_robot_cost
        else:
            robot_cost = self.res_robot_costs[for_res.value]
            count = how_many_can_afford(robot_cost, bank)
            min_count = (
                1 if for_res in (Resource.GEODE, Resource.OBSIDIAN) and count > 0 else 0
            )
            for num in range(min_count, count + 1):
                num_robot_cost = [num * c for c in robot_cost]
                for po, cost in self.purchase_options(
                    [b - c for b, c in zip(bank, num_robot_cost)],
                    Resource(for_res.value - 1),
                ):
                    po[for_res.value] += num
                    yield (
                        po,
                        [c + per_res_c for c, per_res_c in zip(cost, num_robot_cost)],
                    )

    def max_geodes(
        self, time_available: int, robots: PER_RES_COUNT, bank: PER_RES_COUNT
    ) -> int:
        geodes = [bank[Resource.GEODE.value]]
        if time_available > 0:
            for po, cost in self.purchase_options(bank):
                new_robots = [current + new for current, new in zip(robots, po)]
                new_bank = [b + r - c for b, r, c in zip(bank, robots, cost)]
                geodes.append(self.max_geodes(time_available - 1, new_robots, new_bank))
            if time_available > 3:
                print("#" * (time_available - 2) ** 2)
        return max(geodes)

    def search(self, time_available: int) -> int:
        robot_counts = [0] * len(Resource)
        robot_counts[Resource.ORE.value] = 1
        bank = [0] * len(Resource)
        to_visit = deque([(robot_counts, bank, 0)])
        visited = set()
        max_deode = 0
        while to_visit:
            robot_counts, bank, time_to_here = to_visit.popleft()
            visit_key = (tuple(robot_counts), tuple(bank))
            if visit_key in visited:
                continue
            visited.add(visit_key)
            if time_to_here == time_available:
                max_deode = max(max_deode, bank[Resource.GEODE.value])
            else:
                for po, cost in self.purchase_options(bank):
                    new_robots = [
                        current + new for current, new in zip(robot_counts, po)
                    ]
                    new_bank = [b + r - c for b, r, c in zip(bank, robot_counts, cost)]
                    key = (tuple(new_robots), tuple(new_bank))
                    if key not in visited:
                        to_visit.append((new_robots, new_bank, time_to_here + 1))
        return max_deode

    def run_algo(self, time_available: int) -> int:
        robot_counts = [0] * len(Resource)
        robot_counts[Resource.ORE.value] = 1
        bank = [0] * len(Resource)
        for time_left in range(time_available, 0, -1):
            res_to_buy = algo(time_left, bank, robot_counts, self)
            bank = [b + i for b, i in zip(bank, robot_counts)]
            time_disp = time_available - time_left + 1
            if res_to_buy is None:
                print(f"{time_disp} nothing bought {bank}")
            else:
                bank = [
                    b - c for b, c in zip(bank, self.res_robot_costs[res_to_buy.value])
                ]
                robot_counts[res_to_buy.value] += 1
                print(
                    f"{time_disp} bought {res_to_buy} bank {bank} rbots {robot_counts}"
                )

        return bank[Resource.GEODE.value]


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    # time_available = 24
    blueprints: list[Blueprint] = []
    p1, p2 = (0, 0)
    for blueprint_line in input_file.read_text().splitlines():
        bp, costs = blueprint_line.split(":")
        bp_num = int(bp.split()[1])
        robot_info = [[0] * len(Resource) for _ in range(len(Resource))]
        for robot_info_line in costs.split(".")[:-1]:
            _, robot, _, _, cost_info = robot_info_line.split(maxsplit=4)
            cost = robot_info[Resource[robot.upper()].value]
            for cost_part in cost_info.split(" and "):
                num_str, res_str = cost_part.split()
                cost[Resource[res_str.upper()].value] = int(num_str)
        blueprints.append(Blueprint(bp_num, robot_info))

    # print(blueprints[1].run_algo(time_available))
    # foo = 12
    # print([x for x in blueprints[0].purchase_options([7, 7, 7, 7])])
    # print(f"{blueprints[0].search(time_available)=}")
    # robot_counts = [0] * len(Resource)
    # robot_counts[Resource.ORE.value] = 1
    # max_geodes = [bp.num * bp.max_geodes(time_available, robot_counts, [0] * len(Resource))
    #              for bp in blueprints]

    return (p1, p2)


if __name__ == "__main__":
    utils.per_day_main()
