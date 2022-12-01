mod d01;

fn main() {
    let file_path = "../input/d01-example";
    println!("{}", d01::p1(file_path).to_string());
    println!("{}", d01::p2(file_path).to_string());
}
