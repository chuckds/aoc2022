#!/bin/env python3
"""
Advent Of Code 2022 Day 2
"""

from __future__ import annotations

from typing import NamedTuple
from pathlib import Path


repo_root = Path(__file__).parent.parent.parent


def score_that_beats(score: int) -> int:
    return (score % 3) + 1


def score_that_lose_to(score: int) -> int:
    return [x for x in range(1, 4) if x not in (score, score_that_beats(score))][0]


class Move(NamedTuple):
    name: str
    opponent_code: str
    your_code: str
    score: int

    def play(self, other_score: int) -> int:
        result = self.score
        if other_score == self.score:
            return result + 3  # Draw
        elif other_score == score_that_beats(self.score):
            return result  # Lose
        else:
            return result + 6

    def score_given_result(self, result_score: int) -> int:
        total_score = result_score
        if result_score == 3:  # Draw
            return total_score + self.score  # Need to play the same as this move
        elif result_score == 6:  # Win
            return total_score + score_that_beats(self.score)
        else:  # Lose
            return score_that_lose_to(self.score)


moves = [
    Move("rock", "A", "X", 1),
    Move("paper", "B", "Y", 2),
    Move("scissors", "C", "Z", 3),
]

result_scores = {
    "X": 0,
    "Y": 3,
    "Z": 6,
}


move_from_opp_code = {m.opponent_code: m for m in moves}
move_from_your_code = {m.your_code: m for m in moves}


def p1p2(input_file: Path = repo_root / "input" / "d02-example") -> tuple[int, int]:
    inputs = [line.split() for line in input_file.read_text().splitlines()]

    p1_score = 0
    for opp_code, your_code in inputs:
        p1_score += move_from_your_code[your_code].play(move_from_opp_code[opp_code].score)

    p2_score = 0
    for opp_code, result in inputs:
        p2_score += move_from_opp_code[opp_code].score_given_result(result_scores[result])

    return (p1_score, p2_score)
