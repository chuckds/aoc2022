"""
Advent Of Code 2022 Day 6
"""

from __future__ import annotations


from pathlib import Path

import utils


def get_start_of_packet(datastream: str, window_size: int) -> int:
    result = 0
    from_char = 0
    marker_window: list[str] = []
    while from_char < len(datastream):
        read_to = from_char + window_size - len(marker_window)
        marker_window += datastream[from_char:read_to]
        move_forward = -1
        for index, char in enumerate(reversed(marker_window)):
            try:
                dupe_idx = marker_window[: window_size - index - 1].index(char)
                move_forward = max(move_forward, dupe_idx + 1)
            except ValueError:
                # char not present
                continue
        if move_forward == -1:
            # No dupes so this is it!
            return read_to

        from_char = read_to
        marker_window = marker_window[move_forward:]

    return result


def p1p2(input_file: Path = utils.real_input()) -> tuple[list[int], list[int]]:
    p1, p2 = ([], [])
    for ds in input_file.read_text().splitlines():
        p1.append(get_start_of_packet(ds, window_size=4))
        p2.append(get_start_of_packet(ds, window_size=14))

    return (p1, p2)
