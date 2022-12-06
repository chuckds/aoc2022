import re
import json
import pytest
import pathlib
import importlib

from typing import Any


puzzle_re = re.compile(
    r"(?P<day>d[0-9]+)(?P<part>[^ ]+) (?P<input_file>[^ ]+) (?P<result>.*)"
)


def get_puzzle_info(examples: bool) -> list[tuple[str, str, str, str]]:
    day_parts = []
    repo_root = pathlib.Path(__file__).resolve().parent.parent.parent
    with (repo_root / "answers.json").open() as f:
        test_answers = json.load(f)
    for day, function, input_file, expected_result in test_answers:
        expected_result = tuple(expected_result)
        is_example = "example" in input_file
        if is_example and examples:
            day_parts.append(
                (day, function, str(repo_root / "input" / input_file), expected_result)
            )
        elif not is_example and not examples:
            day_parts.append(
                (day, function, str(repo_root / "input" / input_file), expected_result)
            )

    return day_parts


@pytest.mark.parametrize("day,part,input_file,result", get_puzzle_info(True))
def test_puzzle_examples2(day: str, part: str, input_file: str, result: Any) -> None:
    day_mod = importlib.__import__(day)
    part_function = getattr(day_mod, part)
    assert part_function(pathlib.Path(input_file)) == result


@pytest.mark.parametrize("day,part,input_file,result", get_puzzle_info(False))
def test_puzzles(day: str, part: str, input_file: str, result: Any) -> None:
    day_mod = importlib.__import__(day)
    part_function = getattr(day_mod, part)
    assert part_function(pathlib.Path(input_file)) == result
