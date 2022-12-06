mod d01;
mod d02;
mod d03;
mod utils;

use std::collections::HashMap;

use rstest::rstest;

type AoCSolver = fn(&str) -> (i32, i32);

const TEST_MAP: [(&str, AoCSolver); 3] = [
    ("d01", d01::p1p2 as AoCSolver),
    ("d02", d02::p1p2 as AoCSolver),
    ("d03", d03::p1p2 as AoCSolver),
];

fn main() {
    for (day, test_func) in TEST_MAP {
        println!(
            "{} example: {:?}",
            day,
            test_func(&format!("../input/{}-example", day))
        );
        println!(
            "{} full:    {:?}",
            day,
            test_func(&format!("../input/{}", day))
        );
    }

    // Check the answers load
    let _ = test_hash();
}

#[rstest::fixture]
#[once]
fn test_hash() -> HashMap<String, (String, String)> {
    println!("Loading test hash");
    let mut test_hash = HashMap::new();
    let answer_re =
        regex::Regex::new(r"^(?P<part>d[^ ]+) (?P<input_file>[^ ]+) (?P<result>.*)").unwrap();
    //let str_result_re = Regex::new(r"\(\"(?P<p1>.+)\", \"(?P<p2>.+)\"\)").unwrap();
    for line in utils::read_lines("../answers").unwrap() {
        let line = line.unwrap();
        if line.starts_with("#") {
            continue;
        }
        let caps = answer_re.captures(&line).expect("Failed to parse line");
        test_hash.insert(
            // Just keep the first 3 chars, the rest is for python to know what
            // method to call, but that is specified manually for rust
            caps["part"][..3].to_string(),
            (caps["input_file"].to_string(), caps["result"].to_string()),
        );
    }
    test_hash
}

#[rstest]
#[case("d01", d01::p1p2 as AoCSolver)]
#[case("d02", d02::p1p2 as AoCSolver)]
#[case("d03", d03::p1p2 as AoCSolver)]
fn day_test(
    test_hash: &HashMap<String, (String, String)>,
    #[case] day: &str,
    #[case] test_func: AoCSolver,
) {
    let (input_file, expected_result) = test_hash.get(day).expect("Can't find day in hash");
    let int_result_re = regex::Regex::new(r"\((?P<p1>[0-9]+), (?P<p2>[0-9]+)\)").unwrap();
    let retval_caps = int_result_re
        .captures(&expected_result)
        .expect("Failed to parse result");
    let expected_result = (
        retval_caps["p1"].parse::<i32>().unwrap(),
        retval_caps["p2"].parse::<i32>().unwrap(),
    );
    assert_eq!(
        expected_result,
        test_func(&format!("{}{}", "../input/", input_file))
    );
}
