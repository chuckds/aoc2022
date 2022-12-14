use std::cmp::Reverse;
use std::collections::BinaryHeap;

use crate::utils::*;

pub fn p1p2(input_file: &str) -> AoCSolver {
    let mut current_sum: i64 = 0;
    let mut sorted_elves = BinaryHeap::with_capacity(4);

    for line in read_lines(input_file).unwrap() {
        let cal = line.unwrap();
        if cal.is_empty() {
            sorted_elves.push(Reverse(current_sum));
            if sorted_elves.len() > 3 {
                sorted_elves.pop();
            }
            current_sum = 0;
        } else {
            current_sum += cal.parse::<i64>().unwrap();
        }
    }
    sorted_elves.push(Reverse(current_sum));
    if sorted_elves.len() > 3 {
        sorted_elves.pop();
    }

    // what is going on here - this doesn't look good.
    let sorted_elves = sorted_elves.into_sorted_vec();
    // Unpack the values out of Reverse otherwise sum doesn't work - wat?
    let sorted_elves: Vec<i64> = sorted_elves.iter().map(|Reverse(val)| *val).collect();

    AoCSolver::BothParts(
        AoCResult::Number(*sorted_elves.first().unwrap()),
        AoCResult::Number(sorted_elves.iter().sum()),
    )
}
