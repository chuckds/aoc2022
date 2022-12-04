use crate::utils;

pub fn p1p2(input_file: &str) -> (i32, i32) {
    let mut inputs = Vec::new();

    for line in utils::read_lines(input_file).unwrap() {
        let moves = line.unwrap();
        let tokens: Vec<String> = moves.split_whitespace().map(|s| s.to_string()).collect();
        inputs.push(tokens);
    }
    println!("{:?}", inputs);
    //for (opp_code, your_code) in inputs.iter() {
    //    println("opp {}, your {}", opp_code, your_code);
    //}
    (0, 0)
}
