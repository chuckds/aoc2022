use std::collections::HashMap;

use crate::utils;

const OPP_MOVE_MAP: [(char, u8); 3] = [('A', 1), ('B', 2), ('C', 3)];

const YOUR_MOVE_MAP: [(char, u8); 3] = [('X', 1), ('Y', 2), ('Z', 3)];

const SCORE_MAP: [[u8; 3]; 3] = [[3, 6, 0], [0, 3, 6], [6, 0, 3]];

pub fn p1p2(input_file: &str) -> (i32, i32) {
    let mut inputs = Vec::new();
    let opp_move_to_score = HashMap::from(OPP_MOVE_MAP);
    let your_move_to_score = HashMap::from(YOUR_MOVE_MAP);

    for line in utils::read_lines(input_file).unwrap() {
        let moves = line.unwrap();
        let tokens: Vec<char> = moves
            .split_whitespace()
            .map(|s| s.chars().next().unwrap())
            .collect();
        inputs.push((tokens[0], tokens[1]));
    }

    let mut p1: i32 = 0;
    let mut p2: i32 = 0;
    for (opp_code, your_code) in inputs.iter() {
        let your_score = your_move_to_score[your_code];
        let opp_score = opp_move_to_score[opp_code];
        p1 += your_score as i32 + SCORE_MAP[opp_score as usize - 1][your_score as usize - 1] as i32;

        let desired_result = (your_score - 1) * 3;
        let move_needed = SCORE_MAP[opp_score as usize - 1]
            .iter()
            .position(|&s| s == desired_result)
            .unwrap()
            + 1;
        p2 += desired_result as i32 + move_needed as i32;
    }
    (p1, p2)
}
