mod d01;
mod utils;


fn main() {
    let (p1, p2) = d01::p1p2("../input/d01");
    println!("p1: {}, p2: {}", p1, p2);
}

#[test]
fn test() {
    use std::collections::HashMap;
    use regex::Regex;

    let part_to_function = HashMap::from([
        ("d01p1p2", d01::p1p2),
    ]);

    let answer_re = Regex::new(r"^(?P<part>d[^ ]+) (?P<input_file>[^ ]+) (?P<result>.*)").unwrap();
    let result_re = Regex::new(r"\((?P<p1>[0-9]+), (?P<p2>[0-9]+)\)").unwrap();
    for line in utils::read_lines("../answers").unwrap() {
        let line = line.unwrap();
        if let Some(caps) = answer_re.captures(&line) {
            let part = &caps["part"];
            let input_file = &caps["input_file"];
            let result = &caps["result"];
            if let Some(test_func) = part_to_function.get(part) {
                if let Some(retval_caps) = result_re.captures(&result) {
                    let result = (retval_caps["p1"].parse::<i32>().unwrap(),
                                  retval_caps["p2"].parse::<i32>().unwrap());
                    assert_eq!(result,
                              test_func(&format!("{}{}", "../input/", input_file)));
                } else {
                    println!("Failed to parse expected result {}", result);
                }
            } else {
                println!("No function for {}", part);
            }
            
        }

    }
}