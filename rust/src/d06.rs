use crate::utils::*;
use std::collections::HashSet;
use std::str;

pub fn p1p2(input_file: &str) -> AoCSolver {
    let mut p1: Vec<i64> = Vec::new();
    let mut p2: Vec<i64> = Vec::new();

    for line in read_lines(input_file).unwrap() {
        let line = line.unwrap();
        p1.push(get_start_of_packet(&line, 4));
        p2.push(get_start_of_packet(&line, 14));
    }

    AoCSolver::BothParts(AoCResult::NumVec(p1), AoCResult::NumVec(p2))
}

fn get_start_of_packet(ds: &str, window_size: u32) -> i64 {
    let mut result: i64 = 0;
    let mut hs: HashSet<u8> = HashSet::new();

    for (i, window) in ds.as_bytes().windows(window_size as usize).enumerate() {
        if window.iter().all(|x| hs.insert(*x)) {
            result = i as i64;
            break;
        }
        hs.clear();
    }

    result + window_size as i64
}
