"""
Advent Of Code 2022 d13
"""

from __future__ import annotations


from itertools import zip_longest
from typing import Iterable
from pathlib import Path
from dataclasses import dataclass


input_dir = Path(__file__).parent.parent.parent / "input"


@dataclass
class Packet:
    content: str
    at_idx: int = 1

    def next_value(self) -> Iterable[int | Packet]:
        from_idx = self.at_idx
        while from_idx < len(self.content):
            match self.content[from_idx]:
                case "]":
                    break
                case ",":
                    from_idx += 1
                    continue
                case "[":
                    next_packet = Packet(self.content, from_idx + 1)
                    yield next_packet
                    from_idx = next_packet.at_idx + 1  # Skip over the ]
                case other_char:
                    num = ""
                    while other_char.isdigit():
                        num += other_char
                        from_idx += 1
                        other_char = self.content[from_idx]
                    yield int(num)
        self.at_idx = from_idx

    def lt(left, right: Packet) -> bool | None:
        for l_val, r_val in zip_longest(left.next_value(), right.next_value()):
            if l_val is None or r_val is None:
                # One was shorter. If it was Left then it is less than right
                return l_val is None
            if isinstance(l_val, int) and isinstance(r_val, int):
                if l_val == r_val:
                    continue
                else:
                    return l_val < r_val
            if isinstance(l_val, int):
                l_val = Packet(f"[{l_val}]")
            if isinstance(r_val, int):
                r_val = Packet(f"[{r_val}]")
            cmp = l_val.lt(r_val)
            if cmp is None:
                continue
            else:
                return cmp
        # Lists are same length and same elements in them
        return None


def p1p2(input_file: Path = input_dir / "examples" / "d13") -> tuple[int, int]:
    p1, p2 = (0, 0)
    input_lines = input_file.read_text().splitlines()
    packets = [(Packet(input_lines[x]), Packet(input_lines[x + 1]))
               for x in range(0, len(input_lines), 3)]

    for pair_idx, (left, right) in enumerate(packets):
        if left.lt(right):
            p1 += 1 + pair_idx

    return (p1, p2)


if __name__ == "__main__":
    print(p1p2(input_dir / "examples" / "d13"))
    print(p1p2(input_dir / "real" / "d13"))