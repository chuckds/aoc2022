import json
import inspect
import importlib
import timeit
from pathlib import Path


input_dir = Path(__file__).parent.parent.parent / "input"


def get_puzzle_info(examples: bool) -> list[tuple[str, str, str, str]]:
    day_parts = []
    repo_root = Path(__file__).resolve().parent.parent.parent
    with (repo_root / "answers.json").open() as f:
        test_answers = json.load(f)
    for day, function, input_file, expected_result in test_answers:
        expected_result = tuple(expected_result)
        is_example = "example" in input_file
        if is_example and examples:
            day_parts.append(
                (day, function, str(input_dir / input_file), expected_result)
            )
        elif not is_example and not examples:
            day_parts.append(
                (day, function, str(input_dir / input_file), expected_result)
            )

    return day_parts


def input(from_file: str, subdir: str) -> Path:
    day_name = Path(from_file).stem
    return input_dir / subdir / day_name


def real_input(day: str = "") -> Path:
    return input(day if day else inspect.stack()[1].filename, "real")


def example_input(day: str = "") -> Path:
    return input(day if day else inspect.stack()[1].filename, "examples")


def run_all() -> None:
    timing_data = []
    test_calls = []
    for day, part, input_file_str, _ in get_puzzle_info(False):
        day_mod = importlib.__import__(day)
        part_function = getattr(day_mod, part)
        input_file = Path(input_file_str)
        ti = timeit.Timer(lambda: part_function(input_file))
        num_calls, time_taken = ti.autorange()
        timing_data.append((time_taken / num_calls, num_calls, time_taken, day))
        test_calls.append((part_function, input_file))

    ALL_COUNT = 1
    all_days = timeit.timeit(
        lambda: [day(input) for day, input in test_calls], number=ALL_COUNT
    )

    for avg_time, num_calls, total_time, day in sorted(timing_data, reverse=True):
        print(f"{day} avg {avg_time} ({num_calls} calls in {total_time})")

    print(
        f"All {len(test_calls)} days take {all_days / ALL_COUNT} on average ({ALL_COUNT} calls in {all_days})"
    )
    return


if __name__ == "__main__":
    run_all()
