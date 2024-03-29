mod d01;
mod d02;
mod d03;
mod d04;
mod d05;
mod d06;
mod utils;

use crate::utils::*;
use std::collections::HashMap;

use rstest::rstest;

const TEST_MAP: [(&str, AoCSolverFunc, bool); 6] = [
    ("d01", d01::p1p2, true),
    ("d02", d02::p1p2, true),
    ("d03", d03::p1p2, true),
    ("d04", d04::p1p2, true),
    ("d05", d05::p1p2, true),
    ("d06", d06::p1p2, true),
];

fn main() {
    for (day, test_func, do_main) in TEST_MAP {
        println!(
            "{} example: {:?}",
            day,
            test_func(&format!("../input/examples/{}", day))
        );
        if do_main {
            println!(
                "{} full:    {:?}",
                day,
                test_func(&format!("../input/real/{}", day))
            );
        }
    }

    // Check the answers load
    test_hash_json();
}

fn json_to_aocresult(json_val: &json::JsonValue) -> AoCResult {
    match json_val {
        json::JsonValue::Short(a_string) => AoCResult::String(a_string.to_string()),
        json::JsonValue::String(a_string) => AoCResult::String(a_string.to_string()),
        json::JsonValue::Number(_num) => AoCResult::Number(json_val.as_i64().unwrap()),
        json::JsonValue::Array(vec) => {
            AoCResult::NumVec(vec.iter().map(|x| x.as_i64().unwrap()).collect())
        }
        _ => panic!("Unsupported json val"),
    }
}

type TestJsonHash = HashMap<String, Vec<(String, AoCSolver)>>;

#[rstest::fixture]
#[once]
fn test_hash_json() -> TestJsonHash {
    println!("Loading test hash json");

    let json = std::fs::read_to_string("../answers.json").expect("Unable to read json answers");
    let json = json::parse(&json).unwrap();
    let json::JsonValue::Array(ref tests) = json else {
        panic!("Main test array failed to parse");
    };
    let mut test_hash = HashMap::new();
    for test_info in tests {
        let json::JsonValue::Array(ref test_info) = test_info else {
            panic!("Unable to parse test info array: {:?}", test_info);
        };
        let json::JsonValue::Array(ref results) = test_info[3] else {
            panic!("Unable to parse test result");
        };
        test_hash
            .entry(test_info[0].as_str().unwrap().to_string())
            .or_insert(Vec::new())
            .push((
                test_info[2].as_str().unwrap().to_string(),
                AoCSolver::BothParts(
                    json_to_aocresult(&results[0]),
                    json_to_aocresult(&results[1]),
                ),
            ));
    }
    test_hash
}

#[rstest]
#[case("d01", d01::p1p2)]
#[case("d02", d02::p1p2)]
#[case("d03", d03::p1p2)]
#[case("d04", d04::p1p2)]
#[case("d05", d05::p1p2)]
#[case("d06", d06::p1p2)]
fn day_test_json(
    test_hash_json: &TestJsonHash,
    #[case] day: &str,
    #[case] test_func: AoCSolverFunc,
) {
    for (input_file, expected_result) in test_hash_json.get(day).expect("Can't find day in hash") {
        let input_path = format!("{}{}", "../input/", input_file);
        println!("Testing {}", input_file);
        assert_eq!(*expected_result, test_func(&input_path));
    }
}
