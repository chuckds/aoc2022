use std::collections::VecDeque;
use itertools::Itertools;
use crate::utils::*;

#[derive(Debug)]
struct Move {
    num_move: u32,
    from_stack: u32,
    to_stack: u32,
}

pub fn p1p2(input_file: &str) -> AoCSolver {
    let mut p1: i64 = 0;
    let mut p2: i64 = 0;

    let mut stacks: Vec<VecDeque<char>> = Vec::new();
    let mut moves: Vec<Move> = Vec::new();
    let mut stack_phase = true;
    for line in read_lines(input_file).unwrap() {
        let line = line.unwrap();
        if stack_phase {
            for (stack_num, stack_char) in line.chars().skip(1).step_by(4).enumerate() {
                if stack_char == '1' {
                    stack_phase = false;
                    break
                } else {
                    stacks.push(VecDeque::new());
                    if stack_char != ' ' {
                        stacks[stack_num].push_front(stack_char);
                    }
                }
            }
        } else if !line.is_empty() {
            let (num_move, from_stack, to_stack) = line.split(" ")
                .skip(1).step_by(2).map(|x| x.parse::<u32>().unwrap()).next_tuple().unwrap();
            moves.push(Move {num_move: num_move, from_stack: from_stack, to_stack: to_stack});
        }

    }
    println!("{:?}", stacks);
    println!("{:?}", moves);
    AoCSolver::BothParts(AoCResult::Number(p1),
                         AoCResult::Number(p2))
}
