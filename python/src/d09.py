"""
Advent Of Code 2022 Day 9
"""

from __future__ import annotations


from pathlib import Path
from typing import NamedTuple


input_dir = Path(__file__).parent.parent.parent / "input"


class Move(NamedTuple):
    direction: str
    length: int


class Position(NamedTuple):
    x: int
    y: int

    def after_move(self, move: Move) -> list[Position]:
        trail = []
        for step in range(1, move.length + 1):
            match move.direction:
                case "R":
                    trail.append(Position(self.x + step, self.y))
                case "L":
                    trail.append(Position(self.x - step, self.y))
                case "U":
                    trail.append(Position(self.x, self.y + step))
                case "D":
                    trail.append(Position(self.x, self.y - step))
        return trail

    def is_adjacent(self, other: Position) -> bool:
        return (
            self.x - 1 <= other.x <= self.x + 1 and self.y - 1 <= other.y <= self.y + 1
        )

    def get_follow_posn(self, heading_to: Position) -> Position:
        offset = Position(heading_to.x - self.x, heading_to.y - self.y)
        offset = Position(*(n // abs(n) if n else 0 for n in offset))
        return Position(self.x + offset.x, self.y + offset.y)


def p1p2(input_file: Path = input_dir / "d09") -> tuple[int, int]:
    moves = []
    head_trail = [Position(0, 0)]
    for line in input_file.read_text().splitlines():
        dir, len_str = line.split()
        moves.append(Move(dir, int(len_str)))
        head_trail.extend(head_trail[-1].after_move(moves[-1]))

    rope_elements = [Position(0, 0)] * 9
    p1_trail = set([Position(0, 0)])
    tail_end_trail = set([Position(0, 0)])
    for head_posn in head_trail:
        pulled_towards = head_posn
        for idx, rope_element in enumerate(rope_elements):
            if pulled_towards.is_adjacent(rope_element):
                # No movement so the rest of the rope won't change
                break
            else:
                new_posn = rope_element.get_follow_posn(pulled_towards)
                pulled_towards = new_posn
                rope_elements[idx] = new_posn
                if idx == 0:  # p1
                    p1_trail.add(new_posn)
                elif idx == 8:  # p2
                    tail_end_trail.add(new_posn)

    return (len(p1_trail), len(tail_end_trail))
