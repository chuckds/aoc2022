use crate::utils::*;

pub fn p1p2(input_file: &str) -> AoCSolver {
    let mut p1: Vec<i64> = Vec::new();
    let mut p2: Vec<i64> = Vec::new();

    for line in read_lines(input_file).unwrap() {
        let line = line.unwrap();
        p1.push(get_start_of_packet(&line, 4));
        p2.push(get_start_of_packet(&line, 4));
    }

    AoCSolver::BothParts(AoCResult::NumVec(p1),
                         AoCResult::NumVec(p2))
}

fn get_start_of_packet(ds: &str, window_size: u32) -> i64 {
    let result: i64 = 0;
    let from_char: usize = 0;
    result
}