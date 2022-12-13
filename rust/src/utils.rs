use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

#[derive(Debug, PartialEq)]
pub enum AoCResult {
    Number(i64),
    String(String),
    NumVec(Vec<i64>),
}

#[derive(Debug, PartialEq)]
pub enum AoCSolver {
    //SinglePart(AoCResult),
    BothParts(AoCResult, AoCResult),
}

pub type AoCSolverFunc = fn(&str) -> AoCSolver;

pub fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
