"""
Advent Of Code 2022 Day 23
"""

from __future__ import annotations

from typing import NamedTuple, Iterator, Iterable
from pathlib import Path
from collections import deque
import sys
import utils


class Point(NamedTuple):
    x: int
    y: int

    def adjacents(self) -> Iterator[Point]:
        for x_delta in (-1, 0, 1):
            for y_delta in ((-1, 1), (-1, 0, 1))[x_delta]:
                yield Point(self.x + x_delta, self.y + y_delta)

    def norths(self) -> Iterator[Point]:
        for x_delta in (-1, 0, 1):
            yield Point(self.x + x_delta, self.y - 1)

    def souths(self) -> Iterator[Point]:
        for x_delta in (-1, 0, 1):
            yield Point(self.x + x_delta, self.y + 1)

    def wests(self) -> Iterator[Point]:
        for y_delta in (-1, 0, 1):
            yield Point(self.x - 1, self.y + y_delta)

    def easts(self) -> Iterator[Point]:
        for y_delta in (-1, 0, 1):
            yield Point(self.x + 1, self.y + y_delta)

    def the_answer(
        self, offsets: Iterable[Point], elf_posns: set[Point]
    ) -> tuple[Point | None, bool]:
        first_poss_posn = None
        any_elves_around = False
        for offset in offsets:
            dir_posn = Point(self.x + offset.x, self.y + offset.y)
            if dir_posn in elf_posns:
                any_elves_around = True
                continue
            for delta in (-1, 1):
                new_posn = Point(
                    self.x + (delta if offset.x == 0 else offset.x),
                    self.y + (delta if offset.y == 0 else offset.y),
                )
                if new_posn in elf_posns:
                    any_elves_around = True
                    break
            else:  # no break == no elfs in this direction
                if first_poss_posn is None:
                    first_poss_posn = dir_posn
        return first_poss_posn, any_elves_around


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    elf_posns: set[Point] = set()
    for row_idx, line in enumerate(input_file.read_text().splitlines()):
        for char_idx, char in enumerate(line):
            if char == "#":
                elf_posns.add(Point(char_idx, row_idx))

    offsets = deque(
        [
            (Point.norths, Point(0, -1)),
            (Point.souths, Point(0, 1)),
            (Point.wests, Point(-1, 0)),
            (Point.easts, Point(1, 0)),
        ]
    )
    # offsets = deque([Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)])
    elf_moved = True
    round = 0
    while elf_moved:
        elf_moved = False
        next_posns: dict[Point, Point | None] = {}
        for elf in elf_posns:
            # proposed_new_loc, any_elves = elf.the_answer(offsets, elf_posns)
            if any(adj in elf_posns for adj in elf.adjacents()):
                # Find out which direction doesn't have an elf and move towards it
                for dir_func, offset in offsets:
                    if any(adj in elf_posns for adj in dir_func(elf)):
                        # Elf in this direction so don't move here
                        pass
                    else:
                        # No elf in this direction
                        proposed_new_loc = Point(elf.x + offset.x, elf.y + offset.y)
                        if proposed_new_loc in next_posns:
                            # An elf already wants to move so no one can!
                            next_posns[proposed_new_loc] = None
                        else:
                            next_posns[proposed_new_loc] = elf
                        break
            else:
                # No elf around it, do nothing
                pass

        # Update the poitions
        for new_posn, old_posn in next_posns.items():
            if old_posn is not None:
                elf_moved = True
                elf_posns.remove(old_posn)
                elf_posns.add(new_posn)

        # Rotate the offsets
        head = offsets.popleft()
        offsets.append(head)
        round += 1
        if round == 10:
            tl = Point(sys.maxsize, sys.maxsize)
            br = Point(-1, -1)
            for elf in elf_posns:
                tl = Point(min(tl.x, elf.x), min(tl.y, elf.y))
                br = Point(max(br.x, elf.x), max(br.y, elf.y))

            p1 = (br.x - tl.x + 1) * (br.y - tl.y + 1) - len(elf_posns)
    return (p1, round)


if __name__ == "__main__":
    utils.per_day_main()
