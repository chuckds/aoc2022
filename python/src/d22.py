"""
Advent Of Code 2022 Day 22
"""

from __future__ import annotations


import sys
from enum import Enum
from pathlib import Path
from math import sqrt

import utils


cmd_to_rotation_mat = {
    "L": [[0, 1], [-1, 0]],  # Flipped compared to normal since y is mirrored
    "R": [[0, -1], [1, 0]],
    "F": [[-1, 0], [0, -1]],
}


def rotate(rotation: list[list[int]], vec: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sum(mat_val * vec_val for mat_val, vec_val in zip(mat_row, vec)) for mat_row in rotation)


def rotate_about(posn: tuple[int, ...], centre: tuple[int, ...], rotation: list[list[int]]) -> tuple[int, ...]:
    offcentre = tuple(p - c for p, c in zip(posn, centre))
    rotated = rotate(rotation, offcentre)
    return tuple(p + c for p, c in zip(rotated, centre))


class Direction(Enum):
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    UP = (0, -1)


dir_to_score = {
    Direction.RIGHT.value: 0,
    Direction.DOWN.value: 1,
    Direction.LEFT.value: 2,
    Direction.UP.value: 3,
}


MIN = 1 / 2
MAX = -1 / 2


def p1_wrap(posn: tuple[int, int], direction: tuple[int, int], bdl: dict[tuple[int | float, int | float], int]) -> tuple[tuple[int, int], tuple[int, int]]:
    lookup = tuple(-p if d == 0 else d / 2 for p, d in zip(posn, direction))
    new_val = bdl[lookup]  # type: ignore
    return tuple(p if d == 0 else new_val for p, d in zip(posn, direction)), direction  # type: ignore


def p1_walk(posn: tuple[int, int], direction: tuple[int, int], cmds: list[int | str],
            board: dict[tuple[int, int], bool],
            bdl: dict[tuple[int | float, int | float], int]) -> tuple[tuple[int, int], tuple[int, int]]:
    for cmd in cmds:
        if isinstance(cmd, int):
            for _ in range(cmd):
                new_posn = tuple(p + d for p, d in zip(posn, direction))
                is_blocked = board.get(new_posn, None)  # type: ignore
                if is_blocked is None:  # Off the board
                    new_posn, direction = p1_wrap(posn, direction, bdl)
                    is_blocked = board[new_posn]
                if is_blocked:
                    break
                else:
                    posn = new_posn  # type: ignore
        else:
            direction = rotate(cmd_to_rotation_mat[cmd], direction)  # type: ignore
    return posn, direction


def posn_to_face(posn: tuple[int, int], face_size: int, net_width: int) -> int:
    return (posn[1] // face_size) * (net_width // face_size) + (posn[0] // face_size)


def posn_to_facetl(posn: tuple[int, int], face_size: int) -> tuple[int, int]:
    return tuple(face_size * (p // face_size) for p in posn)  # type: ignore


wrap_map = {
    # face, direction -> rotation and translation
    ((8, 0), Direction.UP.value): ("F", (-5, 4)),
    ((8, 0), Direction.LEFT.value): ("L", (-4, 4)),
    ((8, 0), Direction.RIGHT.value): ("F", (7, 8)),
    ((0, 4), Direction.UP.value): ("F", (11, -4)),
    ((0, 4), Direction.LEFT.value): ("R", (15, 7)),
    ((0, 4), Direction.DOWN.value): ("F", (11, 10)),
    ((4, 4), Direction.UP.value): (),
    ((4, 4), Direction.DOWN.value): (),
    ((8, 4), Direction.RIGHT.value): (),
    ((8, 8), Direction.LEFT.value): (),
    ((8, 8), Direction.DOWN.value): (),
    ((12, 8), Direction.UP.value): (),
    ((12, 8), Direction.RIGHT.value): (),
    ((12, 8), Direction.DOWN.value): (),
}


def p1p2(input_file: Path = utils.real_input()) -> tuple[int, int]:
    p1, p2 = (0, 0)
    board: dict[tuple[int, int], bool] = {}
    cmds: list[str | int] = []
    bdl: dict[tuple[int | float, int | float], int] = {}
    net_width = 0
    faces = set()
    for row_num, line in enumerate(input_file.read_text().splitlines()):
        if line and not line[0].isdigit():
            last_col = None
            for col_num, char in enumerate(line):
                if char != " ":
                    if (MIN, -row_num) not in bdl:
                        bdl[(MIN, -row_num)] = col_num
                    bdl[(-col_num, MIN)] = min(row_num, bdl.get((-col_num, MIN), sys.maxsize))
                    bdl[(-col_num, MAX)] = max(row_num, bdl.get((-col_num, MAX), -1))
                    blocked = True if char == "#" else False
                    board[(col_num, row_num)] = blocked
                    last_col = col_num
            if last_col is not None:
                bdl[(MAX, -row_num)] = last_col
                net_width = max(net_width, last_col + 1)
        elif line:
            num = ""
            for char in line:
                if char.isdigit():
                    num += char
                else:
                    if num:
                        cmds.append(int(num))
                    cmds.append(char)
                    num = ""
            if num:
                cmds.append(int(num))

    face_size = int(sqrt(len(board) // 6))
    for posn in board.keys():
        faces.add(posn_to_facetl(posn, face_size))

    posn, direction = p1_walk((bdl[(MIN, -0)], 0), (1, 0), cmds, board, bdl)

    p1 = (posn[1] + 1) * 1000 + (posn[0] + 1) * 4 + dir_to_score[direction]
    return (p1, p2)


if __name__ == "__main__":
    utils.per_day_main()
