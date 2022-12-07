mod d01;
mod d02;
mod d03;
mod utils;

use std::collections::HashMap;

use rstest::rstest;

type AoCSolver = fn(&str) -> (i32, i32);

#[derive(Debug)]
enum AoCResult {
    Number(i32),
    String(String),
    NumVec(Vec<i64>),
}

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
    println!("THJ {:?}", test_hash_json());
}

fn json_to_aocresult(json_val: &json::JsonValue) -> AoCResult {
    match json_val {
        json::JsonValue::Short(a_string) => AoCResult::String(a_string.to_string()),
        json::JsonValue::Number(_num) => AoCResult::Number(json_val.as_i32().unwrap()),
        json::JsonValue::Array(vec) => {
            AoCResult::NumVec(vec.iter().map(|x| x.as_i64().unwrap()).collect())
        }
        _ => panic!("Unsupported json val"),
    }
}

type TestJsonHash = HashMap<String, Vec<(String, (AoCResult, AoCResult))>>;

#[rstest::fixture]
#[once]
fn test_hash_json() -> TestJsonHash {
    println!("Loading test hash json");
    let mut test_hash = HashMap::new();
    let json = std::fs::read_to_string("../answers.json").expect("Unable to read json answers");
    let json = json::parse(&json).unwrap();
    if let json::JsonValue::Array(ref tests) = json {
        for test_info in tests {
            if let json::JsonValue::Array(ref test_info) = test_info {
                if let json::JsonValue::Array(ref results) = test_info[3] {
                    test_hash
                        .entry(test_info[0].as_str().unwrap().to_string())
                        .or_insert(Vec::new())
                        .push((
                            test_info[2].as_str().unwrap().to_string(),
                            (
                                json_to_aocresult(&results[0]),
                                json_to_aocresult(&results[1]),
                            ),
                        ));
                }
            }
        }
    }
    test_hash
}

#[rstest]
#[case("d01", d01::p1p2 as AoCSolver)]
#[case("d02", d02::p1p2 as AoCSolver)]
#[case("d03", d03::p1p2 as AoCSolver)]
fn day_test_json(test_hash_json: &TestJsonHash, #[case] day: &str, #[case] test_func: AoCSolver) {
    for (input_file, expected_result) in test_hash_json.get(day).expect("Can't find day in hash") {
        let input_path = format!("{}{}", "../input/", input_file);
        println!("Testing {}", input_file);
        match expected_result {
            (AoCResult::Number(n1), AoCResult::Number(n2)) => {
                assert_eq!((*n1, *n2), test_func(&input_path))
            }
            _ => panic!("Unsupported result type"),
        }
    }
}
