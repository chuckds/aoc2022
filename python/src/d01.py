#!/bin/env python3
"""
Advent Of Code 2021 Day 1
"""

import sys
import time
import collections


def count_increasing_sliding_windows(filename: str, window_size: int) -> int:
    increasing: int = 0

    with open(filename) as f:
        depths = collections.deque(int(next(f))
                                   for _ in range(window_size))
        for line in f:
            depth = int(line)
            # The only elements two consecutive sliding windows differ by is
            # the first and last, so only these need to be compared to see
            # which window is bigger
            if depth > depths.popleft():
                increasing += 1
            depths.append(depth)

    return increasing


def p1(input_file: str) -> int:
    return count_increasing_sliding_windows(input_file, 1)


def p2(input_file: str) -> int:
    return count_increasing_sliding_windows(input_file, 3)


def main(cli_args: list[str]) -> int:
    start = time.perf_counter()
    print(p1(cli_args[0]))
    print(p2(cli_args[0]))
    stop = time.perf_counter()
    print(f"Elapsed: {stop - start:.6f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))