use std::collections::HashSet;

use crate::utils;

fn char_to_prio(a_char: char) -> i32 {
    let offset = if a_char.is_ascii_lowercase() {96} else {38};
    return a_char as i32 - offset
}

pub fn p1p2(input_file: &str) -> (i32, i32) {
    let mut p1: i32 = 0;
    let mut p2: i32 = 0;

    let mut group_bags: Vec<HashSet<char>> = Vec::with_capacity(3);
    for line in utils::read_lines(input_file).unwrap() {
        let item_list = line.unwrap();

        let comp1 = &item_list[..(item_list.len() / 2)];
        let comp2 = &item_list[(item_list.len() / 2)..];
        let comp1: HashSet<char> = HashSet::from_iter(comp1.chars());
        let comp2: HashSet<char> = HashSet::from_iter(comp2.chars());
        let common_char = comp1.intersection(&comp2).next().expect("No items in common");
        p1 += char_to_prio(*common_char);

        // Part 2
        group_bags.push(HashSet::from_iter(item_list.chars()));
        if group_bags.len() == 3 {
            for a_char in &group_bags[0] {
                if group_bags[1].contains(&a_char) && group_bags[2].contains(&a_char) {
                    p2 += char_to_prio(*a_char);
                    break
                }
            }
            group_bags.clear();
        }
    }
    (p1, p2)
}
