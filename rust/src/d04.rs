use itertools::Itertools;

use crate::utils::*;

pub fn p1p2(input_file: &str) -> AoCSolver {
    let mut p1: i64 = 0;
    let mut p2: i64 = 0;

    for line in read_lines(input_file).unwrap() {
        let line = line.unwrap();
        let (elf1, elf2) = line.split(",").next_tuple().unwrap();
        let (elf1_start, elf1_end) = range_str_parse(elf1);
        let (elf2_start, elf2_end) = range_str_parse(elf2);

        if elf1_start <= elf2_start && elf1_end >= elf2_end ||
           elf2_start <= elf1_start && elf2_end >= elf1_end {
            p1 += 1;
        }
        if elf1_end >= elf2_start && elf1_start <= elf2_end ||
           elf2_end >= elf1_start && elf2_start <= elf1_end {
            p2 += 1;
        }

    }

    AoCSolver::BothParts(AoCResult::Number(p1),
                         AoCResult::Number(p2))
}

fn range_str_parse(range: &str) -> (i64, i64) {
    range.split("-")
            .map(|x| x.parse::<i64>().unwrap())
            .collect_tuple().unwrap()
}