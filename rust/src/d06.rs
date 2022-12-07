use crate::utils::*;

pub fn p1p2(input_file: &str) -> AoCSolver {
    let mut p1: i64 = 0;
    let mut p2: i64 = 0;

    for line in utils::read_lines(input_file).unwrap() {
        let line = line.unwrap();
    }

    AoCSolver::BothParts(AoCResult::Number(p1),
                         AoCResult::Number(p2))
}
