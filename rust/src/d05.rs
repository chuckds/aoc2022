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
                    if stack_num >= stacks.len() {
                        stacks.push(VecDeque::new());
                    }
                    if stack_char != ' ' {
                        stacks[stack_num].push_back(stack_char);
                    }
                }
            }
        } else if !line.is_empty() {
            let (num_move, from_stack, to_stack) = line.split(" ")
                .skip(1).step_by(2).map(|x| x.parse::<u32>().unwrap()).next_tuple().unwrap();
            moves.push(Move {num_move: num_move, from_stack: from_stack - 1, to_stack: to_stack - 1});
        }
    }

    let mut p1_stacks: Vec<VecDeque<char>> = Vec::new();
    for stack in &stacks {
        p1_stacks.push(stack.clone());
    }

    for a_move in moves {
        let chars_to_move = p1_stacks[a_move.from_stack as usize].drain(..a_move.num_move as usize).collect::<Vec<_>>();
        for char_to_move in chars_to_move {
            p1_stacks[a_move.to_stack as usize].push_front(char_to_move);
        }
        
        let chars_to_move = stacks[a_move.from_stack as usize].drain(..a_move.num_move as usize).collect::<Vec<_>>();
        for char_to_move in chars_to_move.iter().rev() {
            stacks[a_move.to_stack as usize].push_front(*char_to_move);
        }
    }

    let p1 = p1_stacks.iter().map(|x| x.front().unwrap()).collect::<String>();
    let p2 = stacks.iter().map(|x| x.front().unwrap()).collect::<String>();
    AoCSolver::BothParts(AoCResult::String(p1),
                         AoCResult::String(p2))
}
