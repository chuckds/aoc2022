"""
Advent Of Code 2022 Day 21
"""

from __future__ import annotations


import operator
from dataclasses import dataclass, field
from typing import Callable, cast
from pathlib import Path

import utils


MONKEY_MATH_OP = Callable[[int, int], int]


op_to_func: dict[str, MONKEY_MATH_OP] = {
    "*": operator.mul,
    "/": operator.floordiv,
    "+": operator.add,
    "-": operator.sub,
}


# Index by which dependecy is resolvable
op_to_inverse: dict[MONKEY_MATH_OP, tuple[MONKEY_MATH_OP, MONKEY_MATH_OP]] = {
    operator.mul: (operator.floordiv, operator.floordiv),
    operator.floordiv: (
        lambda result, dep: operator.floordiv(dep, result),
        operator.mul,
    ),
    operator.add: (operator.sub, operator.sub),
    operator.sub: (lambda result, dep: operator.sub(dep, result), operator.add),
}


@dataclass
class Monkey:
    name: str
    monkeys: dict[str, Monkey]

    def get_val(self) -> int:
        return 0

    def depends_on_variable(self, name: str) -> bool:
        return False

    def find_inverse(self, result: int) -> int:
        return 0


@dataclass
class MonkeyVal(Monkey):
    number: int

    def get_val(self) -> int:
        return self.number

    def depends_on_variable(self, name: str) -> bool:
        return self.name == name

    def find_inverse(self, result: int) -> int:
        return result


@dataclass
class MonkeyDepends(Monkey):
    op: MONKEY_MATH_OP
    depends: tuple[str, str]
    _dep_var: int = field(default=0, init=False)
    _dep_not_var: int = field(default=0, init=False)

    def get_val(self) -> int:
        return self.op(
            self.monkeys[self.depends[0]].get_val(),
            self.monkeys[self.depends[1]].get_val(),
        )

    def depends_on_variable(self, name: str) -> bool:
        res = False
        for dep_idx, dep_monkey in enumerate(self.monkeys[dep] for dep in self.depends):
            if dep_monkey.depends_on_variable(name):
                res = True
                self._dep_var = dep_idx
            else:
                self._dep_not_var = dep_idx
        return res

    def find_inverse(self, result: int) -> int:
        # What value does the unresolvable dependency need to be to give result?
        inv_op = op_to_inverse[self.op][self._dep_not_var]
        sub_result = inv_op(
            result, self.monkeys[self.depends[self._dep_not_var]].get_val()
        )
        return self.monkeys[self.depends[self._dep_var]].find_inverse(sub_result)


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    monkeys: dict[str, Monkey] = {}
    for line in input_file.read_text().splitlines():
        monkey, op_str = line.split(": ")
        try:
            val = int(op_str)
            monkeys[monkey] = MonkeyVal(monkey, monkeys, val)
        except ValueError:
            dep1, op, dep2 = op_str.split()
            monkeys[monkey] = MonkeyDepends(
                monkey, monkeys, op_to_func[op], (dep1, dep2)
            )

    root_monkey = cast(MonkeyDepends, monkeys["root"])
    p1 = root_monkey.get_val()

    YOUR_NAME = "humn"
    required_val = 0
    to_resolve: Monkey = Monkey("invalid", monkeys)
    for root_dep_monkey in (monkeys[dep] for dep in root_monkey.depends):
        if root_dep_monkey.depends_on_variable(YOUR_NAME):
            to_resolve = root_dep_monkey
        else:  # If it doesn't depend on our value then get the value that needs to be equaled
            required_val = root_dep_monkey.get_val()

    p2 = to_resolve.find_inverse(required_val)

    return (p1, p2)


if __name__ == "__main__":
    utils.per_day_main()
