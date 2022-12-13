"""
Advent Of Code 2022 d13
"""

from __future__ import annotations


from itertools import zip_longest
from typing import Iterable
from pathlib import Path
from dataclasses import dataclass

import utils


real = utils.real_input()


@dataclass
class Packet:
    content: str
    at_idx: int = 1
    end_idx: int = 0

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
                    from_idx = next_packet.end_idx + 1  # Skip over the ]
                case other_char:
                    num = ""
                    while other_char.isdigit():
                        num += other_char
                        from_idx += 1
                        other_char = self.content[from_idx]
                    yield int(num)
        self.end_idx = from_idx

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


def p1p2(input_file: Path = real) -> tuple[int, int]:
    p1 = 0
    input_lines = input_file.read_text().splitlines()
    packets = [
        (Packet(input_lines[x]), Packet(input_lines[x + 1]))
        for x in range(0, len(input_lines), 3)
    ]

    for pair_idx, (left, right) in enumerate(packets):
        if left.lt(right):
            p1 += 1 + pair_idx

    divider = Packet("[[2]]")
    gt_div1 = []
    divider_idx = 1
    for packet in (packet for packet_pair in packets for packet in packet_pair):
        if packet.lt(divider):
            divider_idx += 1
        else:
            gt_div1.append(packet)
    decoder_key = divider_idx

    divider_idx += 1  # 2nd divider is bigger than the first so index + 1
    divider = Packet("[[6]]")
    divider_idx += len([1 for p in gt_div1 if p.lt(divider)])
    decoder_key *= divider_idx

    return (p1, decoder_key)


if __name__ == "__main__":
    print(p1p2(utils.example_input()))
    print(p1p2(real))
