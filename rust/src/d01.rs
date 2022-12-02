use std::cmp::Reverse;
use std::collections::BinaryHeap;

use crate::utils;

pub fn p1p2(input_file: &str) -> (i32, i32) {
    let mut current_sum = 0;
    let mut sorted_elves = BinaryHeap::with_capacity(4);

    for line in utils::read_lines(input_file).unwrap() {
        let cal = line.unwrap();
        if cal.is_empty() {
            sorted_elves.push(Reverse(current_sum));
            if sorted_elves.len() > 3 {
                sorted_elves.pop();
            }
            current_sum = 0;
        } else {
            current_sum += cal.parse::<i32>().unwrap();
        }
    }
    sorted_elves.push(Reverse(current_sum));
    if sorted_elves.len() > 3 {
        sorted_elves.pop();
    }

    // what is going on here - this doesn't look good.
    let sorted_elves = sorted_elves.into_sorted_vec();
    // Unpack the values out of Reverse otherwise sum doesn't work - wat?
    let sorted_elves: Vec<i32> = sorted_elves.iter().map(|Reverse(val)| *val).collect();

    (*sorted_elves.first().unwrap(), sorted_elves.iter().sum())
}

#[test]
fn d01_test() {
    assert_eq!((24000, 45000), p1p2("../input/d01-example"));
    assert_eq!((71924, 210406), p1p2("../input/d01"));
}
