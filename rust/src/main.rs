mod d01;
mod d02;
mod utils;

fn main() {
    println!("{:?}", d01::p1p2("../input/d01-example"));
    println!("{:?}", d02::p1p2("../input/d02-example"));
}

type AoCSolver = fn(&str) -> (i32, i32);

#[test]
fn test() {
    use regex::Regex;
    use std::collections::HashMap;

    let part_to_function: HashMap<&str, AoCSolver> = HashMap::from([
        ("d01p1p2", d01::p1p2 as AoCSolver),
        ("d02p1p2", d02::p1p2 as AoCSolver),
    ]);

    let answer_re = Regex::new(r"^(?P<part>d[^ ]+) (?P<input_file>[^ ]+) (?P<result>.*)").unwrap();
    let int_result_re = Regex::new(r"\((?P<p1>[0-9]+), (?P<p2>[0-9]+)\)").unwrap();
    //let str_result_re = Regex::new(r"\(\"(?P<p1>.+)\", \"(?P<p2>.+)\"\)").unwrap();
    for line in utils::read_lines("../answers").unwrap() {
        let line = line.unwrap();
        if let Some(caps) = answer_re.captures(&line) {
            let part = &caps["part"];
            let input_file = &caps["input_file"];
            let result = &caps["result"];
            if let Some(test_func) = part_to_function.get(part) {
                if let Some(retval_caps) = int_result_re.captures(&result) {
                    let result = (
                        retval_caps["p1"].parse::<i32>().unwrap(),
                        retval_caps["p2"].parse::<i32>().unwrap(),
                    );
                    assert_eq!(result, test_func(&format!("{}{}", "../input/", input_file)));
                //} else if let Some(retval_caps) = str_result_re.captures(&result) {
                //    let result = (
                //        &retval_caps["p1"],
                //        &retval_caps["p2"],
                //    );
                //    assert_eq!(result, test_func(&format!("{}{}", "../input/", input_file)));
                } else {
                    println!("Failed to parse expected result {}", result);
                }
            } else {
                println!("No function for {}", part);
            }
        } else {
            println!("Failed to parse {}", line);
        }
    }
}
