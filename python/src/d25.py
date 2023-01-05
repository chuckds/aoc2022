"""
Advent Of Code 2022 Day 25
"""

from __future__ import annotations


from pathlib import Path
from dataclasses import dataclass
from functools import cached_property
from itertools import zip_longest
from collections import deque

import utils


@dataclass
class Snafu:
    val: str

    char_to_digit = {
        "0": 0,
        "1": 1,
        "2": 2,
        "-": -1,
        "=": -2,
    }

    dig_sum_to_char = {
        -5: ("0", -1),
        -4: ("1", -1),
        -3: ("2", -1),
        -2: ("=", 0),
        -1: ("-", 0),
        0: ("0", 0),
        1: ("1", 0),
        2: ("2", 0),
        3: ("=", 1),
        4: ("-", 1),
        5: ("0", 1),
    }

    @cached_property
    def digits(self) -> list[int]:
        return [self.char_to_digit[char] for char in self.val]

    def __int__(self) -> int:
        pow_5 = 1
        val = 0
        for dig in reversed(self.digits):
            val += dig * pow_5
            pow_5 *= 5
        return val

    def __add__(self, other: Snafu) -> Snafu:
        carry = 0
        new_digits: deque[str] = deque([])
        for this_dig, other_dig in zip_longest(
            reversed(self.digits), reversed(other.digits), fillvalue=0
        ):
            new_dig, carry = self.dig_sum_to_char[this_dig + other_dig + carry]
            new_digits.appendleft(new_dig)
        if carry:
            new_digits.appendleft(self.dig_sum_to_char[carry][0])

        return Snafu("".join(new_digits))

    @classmethod
    def from_int(cls, an_int: int) -> Snafu:
        val = an_int
        new_digits: deque[str] = deque([])
        while val:
            div5, mod5 = divmod(val, 5)
            new_dig, carry = cls.dig_sum_to_char[mod5]
            new_digits.appendleft(new_dig)
            val = div5 + carry
        return Snafu("".join(new_digits))


def p1p2(input_file: Path = utils.real_input()) -> tuple[str, int]:
    p2 = 0
    numbers = [Snafu(line) for line in input_file.read_text().splitlines()]
    sn_sum = Snafu("0")
    for n in numbers:
        sn_sum += n
    return (sn_sum.val, p2)


if __name__ == "__main__":
    utils.per_day_main()
