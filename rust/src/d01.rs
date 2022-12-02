use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::VecDeque;


pub fn p1p2(input_file: &str) -> (i32, i32) {
    let increasing = 0;
    let depths: VecDeque<u32> = VecDeque::new();
    let lines = read_lines(input_file);
    // Consumes the iterator, returns an (Optional) String
    for cal in lines {
        let cal = cal.parse::<i32>().unwrap();
    }
    (34, 12)
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}