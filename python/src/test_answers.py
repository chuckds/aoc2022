import re
import pytest
import pathlib
import importlib


puzzle_re = re.compile(r"(?P<day>d[0-9]+)(?P<part>[^ ]+) (?P<input_file>[^ ]+) (?P<result>.*)")


def get_puzzle_info(examples: bool) -> list[tuple[str, str, str, str]]:
    day_parts = []
    repo_root = pathlib.Path(__file__).resolve().parent.parent.parent
    with open(repo_root / 'answers') as f:
        for line in f:
            m = puzzle_re.match(line)
            if m is None:
                continue
            day = m.group('day')
            part = m.group('part')
            input_file = m.group('input_file')
            is_example = 'example' in input_file
            result = m.group('result')
            if is_example and examples:
                day_parts.append((day, part, str(repo_root / "input" / input_file), result))
            elif not is_example and not examples:
                day_parts.append((day, part, str(repo_root / "input" / input_file), result))

    return day_parts


@pytest.mark.parametrize("day,part,input_file,result", get_puzzle_info(True))
def test_puzzle_examples(day: str, part: str, input_file: str, result: str) -> None:
    day_mod = importlib.__import__(day)
    part_function = getattr(day_mod, part)
    result_val = eval(result)
    assert part_function(input_file) == result_val


@pytest.mark.parametrize("day,part,input_file,result", get_puzzle_info(False))
def test_puzzles(day: str, part: str, input_file: str, result: str) -> None:
    day_mod = importlib.__import__(day)
    part_function = getattr(day_mod, part)
    result_val = eval(result)
    assert part_function(input_file) == result_val
