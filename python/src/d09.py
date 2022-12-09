"""
Advent Of Code 2022 d09
"""

from __future__ import annotations


from pathlib import Path
from typing import NamedTuple


input_dir = Path(__file__).parent.parent.parent / "input"

"""
..DMD...
.DAAAD.
.MATAM.
.DAAAD.
..DMD.
"""

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
        return self.x - 1 <= other.x <= self.x + 1 and self.y - 1 <= other.y <= self.y + 1


def get_follow_posn(from_posn: Position, heading_to: Position) -> Position:
    x_offset = heading_to.x - from_posn.x
    y_offset = heading_to.y - from_posn.y
    x_offset = x_offset // abs(x_offset) if x_offset else 0
    y_offset = y_offset // abs(y_offset) if y_offset else 0
    return Position(from_posn.x + x_offset, from_posn.y + y_offset)


def p1p2(input_file: Path = input_dir / "d09") -> tuple[int, int]:
    p2 = 0
    moves = []
    head_trail = [Position(0, 0)]
    for line in input_file.read_text().splitlines():
        dir, len_str = line.split()
        moves.append(Move(dir, int(len_str)))
        head_trail.extend(head_trail[-1].after_move(moves[-1]))
    print(head_trail)
    tail_trail = [Position(0, 0)]
    trail_elements = [Position(0, 0)] * 9
    tail_end_trail = [Position(0, 0)]
    for head_posn in head_trail:
        if not head_posn.is_adjacent(tail_trail[-1]):
            tail_trail.append(get_follow_posn(tail_trail[-1], head_posn))

    unique_posn = set(tail_trail)
    return (len(unique_posn), p2)
