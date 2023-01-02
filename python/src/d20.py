"""
Advent Of Code 2022 Day 20
"""

from __future__ import annotations


from pathlib import Path
from dataclasses import dataclass
from itertools import islice

import utils


grove_coord_indicies = (1000, 2000, 3000)
decryption_key = 811589153


@dataclass
class EncyptedNumber:
    value: int
    index: int


def parse_numbers(input_file: Path) -> tuple[list[EncyptedNumber], EncyptedNumber]:
    numbers: list[EncyptedNumber] = []
    zero_num: EncyptedNumber = EncyptedNumber(0, 0)
    for line_idx, line in enumerate(input_file.read_text().splitlines()):
        new_num = EncyptedNumber(int(line), line_idx)
        numbers.append(new_num)
        if new_num.value == 0:
            zero_num = new_num
    return numbers, zero_num


def mix_num_in_numbers(num: EncyptedNumber, numbers: list[EncyptedNumber]) -> None:
    if num.value == 0:
        new_idx = num.index
    else:
        new_idx = (num.index + num.value - 1) % (len(numbers) - 1) + 1

    if new_idx < num.index:
        for moved_num in islice(numbers, new_idx, num.index):
            moved_num.index = (moved_num.index + 1) % len(numbers)
    elif new_idx > num.index:
        for moved_num in islice(numbers, num.index + 1, new_idx + 1):
            moved_num.index = (moved_num.index - 1) % len(numbers)
    numbers.insert(new_idx, numbers.pop(num.index))
    num.index = new_idx


def mix_numbers(numbers: list[EncyptedNumber]) -> None:
    for num in numbers[:]:
        mix_num_in_numbers(num, numbers)


def first(input_file: Path) -> tuple[int, int]:
    p1, p2 = (0, 0)
    numbers, zero_num = parse_numbers(input_file)
    mix_numbers(numbers)

    p1 = sum(
        numbers[(zero_num.index + raw_idx) % len(numbers)].value
        for raw_idx in grove_coord_indicies
    )
    return (p1, p2)


@dataclass(slots=True)
class EncryptedNum:
    value: int
    prev: EncryptedNum
    next: EncryptedNum
    move_num: int = 0
    forward: bool = True

    def set_move_params(self, list_len: int, flip_at: int) -> None:
        self.forward = self.value >= 0
        self.move_num = abs(self.value) % (list_len - 1)
        if self.move_num > flip_at:
            self.move_num = list_len - self.move_num - 1
            self.forward = not self.forward


def get_number_list(input_file: Path) -> tuple[list[EncryptedNum], EncryptedNum]:
    numbers: list[EncryptedNum] = []
    prev: EncryptedNum | None = None
    zero_num: EncryptedNum = EncryptedNum(0, None, None)  # type: ignore
    for line in input_file.read_text().splitlines():
        if prev is None:
            new_num = EncryptedNum(int(line), None, None)  # type: ignore
        else:
            new_num = EncryptedNum(int(line), prev, None)  # type: ignore
            prev.next = new_num
        numbers.append(new_num)
        prev = new_num
        if new_num.value == 0:
            zero_num = new_num
    # Loop around
    numbers[0].prev = new_num
    new_num.next = numbers[0]
    return numbers, zero_num


def mix(numbers: list[EncryptedNum]) -> None:
    for num in numbers:
        if num.move_num == 0:
            pass
        else:
            # Remove it from the list
            num.prev.next = num.next
            num.next.prev = num.prev
            current_num = num
            if num.forward:
                for _ in range(num.move_num):
                    current_num = current_num.next
            else:
                for _ in range(num.move_num + 1):
                    current_num = current_num.prev
            # insert after current_num
            num.next = current_num.next
            num.prev = current_num
            num.next.prev = num
            current_num.next = num


def get_val(zero: EncryptedNum) -> int:
    current_num = zero
    vals = []
    prev_index = 0
    for index in grove_coord_indicies:
        for _ in range(index - prev_index):
            current_num = current_num.next
        prev_index = index
        vals.append(current_num.value)

    return sum(vals)


def second(input_file: Path) -> tuple[int, int]:
    p1, p2 = (0, 0)

    numbers, zero_num = get_number_list(input_file)
    flip_at = (len(numbers) // 2) + 4
    for num in numbers:
        num.set_move_params(len(numbers), flip_at)

    mix(numbers)
    p1 = get_val(zero_num)

    # Reset
    prev = numbers[-1]
    for num in numbers:
        num.prev = prev
        prev.next = num
        prev = num
        num.value *= decryption_key
        num.set_move_params(len(numbers), flip_at)

    for _ in range(10):
        mix(numbers)
    p2 = get_val(zero_num)

    return (p1, p2)


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    p1, p2 = second(input_file)
    return (p1, p2)


if __name__ == "__main__":
    utils.per_day_main()
