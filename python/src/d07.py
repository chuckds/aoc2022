#!/bin/env python3
"""
Advent Of Code 2022 Day 7
"""

from __future__ import annotations


from dataclasses import dataclass, field
from pathlib import Path


repo_root = Path(__file__).parent.parent.parent

@dataclass
class Dir:
    name: str
    parent: Dir | None = None
    direct_size: int = 0
    subdirs: dict[str, Dir] = field(default_factory=dict)
    too_big: bool = False

    def child_dir(self, dir_name: str) -> Dir:
        return self.subdirs[dir_name]

    def add_child_dir(self, dir_name: str) -> Dir:
        new_dir = Dir(dir_name, self)
        self.subdirs[dir_name] = new_dir
        return new_dir


def collapse_tree_to_limit(size_limit: int, dirs: list[Dir]) -> int:
    sum_of_dirs = 0
    # Invarient: directories in this list have no child dirs!
    dirs_to_check = [d for d in dirs if not d.subdirs]
    while dirs_to_check:
        dir = dirs_to_check.pop()
        if dir.direct_size > size_limit:
            if dir.parent is not None:
                dir.parent.too_big = True
        else:
            sum_of_dirs += dir.direct_size  # This dir counts
            if dir.parent and not dir.parent.too_big:
                dir.parent.direct_size += dir.direct_size
                del dir.parent.subdirs[dir.name]
                if dir.parent.direct_size > size_limit:
                    dir.parent.too_big = True
                elif not dir.parent.subdirs:
                    dirs_to_check.append(dir.parent)
    return sum_of_dirs


DISK_SIZE = 70000000
FREE_SPACE_REQUIRED = 30000000


def p1p2(input_file: Path = repo_root / "input" / "d07-example") -> tuple[int, int]:
    p1, p2 = (0, 0)
    all_dirs: list[Dir] = []
    current_dir: Dir | None = None
    total_space_used = 0
    for terminal_line in input_file.read_text().splitlines():
        if terminal_line.startswith("$ cd "):
            newdir = terminal_line[5:]
            if newdir == "..":
                assert current_dir is not None
                current_dir = current_dir.parent
            elif current_dir:
                current_dir = current_dir.child_dir(newdir)
            else:
                # First line case
                current_dir = Dir(newdir)
                all_dirs.append(current_dir)
        elif terminal_line.startswith("$ ls"):
            # Don't need to do anything
            pass
        elif terminal_line.startswith("dir "):
            assert current_dir is not None
            subdir = current_dir.add_child_dir(terminal_line[4:])
            all_dirs.append(subdir)
        else:
            assert current_dir is not None
            size, _ = terminal_line.split()
            size_i = int(size)
            total_space_used += size_i
            current_dir.direct_size += size_i

    space_to_free = FREE_SPACE_REQUIRED - (DISK_SIZE - total_space_used)
    print(f"{total_space_used=} {space_to_free=}")

    p1 = collapse_tree_to_limit(100000, all_dirs)
    print(all_dirs)

    return (p1, p2)
