# Advent of Code 2022

Back again.

https://adventofcode.com/2022/

Going to try Rust as well this year, not clear how both will be handled

Run tests with:
```
./Taskfile
```

This runs mypy, pytest and cargo test for rust. Also set up the repo with the precommit check
```
./Taskfile initrepo
```

Make sure rust and python are formatted in a standard way:
```
./Taskfile fmt
```

Puzzle input shouldn't be shared, so it is no longer committed to the repo.
Use [aoc-cli](https://github.com/scarvalhojr/aoc-cli) to download input for a given day:
```
aoc download -I --input-file -d {day-num} input/real/${DAY}
```