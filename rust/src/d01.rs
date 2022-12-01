use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::VecDeque;

pub fn p1(input_file: &str) -> i32 {
    count_increasing_sliding_windows(input_file, 1)
}

pub fn p2(input_file: &str) -> i32 {
    count_increasing_sliding_windows(input_file, 3)
}

fn count_increasing_sliding_windows(input_file: &str, window_size: u32) -> i32 {
    let increasing = 0;
    let depths: VecDeque<u32> = VecDeque::new();
    if let Ok(lines) = read_lines(input_file) {
        // Consumes the iterator, returns an (Optional) String
        for line in lines {
            if let Ok(depth) = line {
                let depth = depth.parse::<u32>().unwrap();
                if depths.len() == window_size.try_into().unwrap() {
                    if let Ok(front_depth) = depths.pop_front() {
                        if depth > front_depth {
                            increasing += 1;
                        }
                    }
                }
                depths.push_back(depth);
            }
        }
    }
    increasing
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}