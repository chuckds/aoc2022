use criterion::{black_box, criterion_group, criterion_main, Criterion};

mod d01;
mod d02;
mod d03;
mod d04;
mod d05;
mod d06;
mod utils;

const BENCH_MAP: [(&str, utils::AoCSolverFunc); 6] = [
    ("d01", d01::p1p2),
    ("d02", d02::p1p2),
    ("d03", d03::p1p2),
    ("d04", d04::p1p2),
    ("d05", d05::p1p2),
    ("d06", d06::p1p2),
];

pub fn criterion_benchmark(c: &mut Criterion) {
    for (day, test_func) in BENCH_MAP {
        c.bench_function(day, |b| {
            b.iter(|| test_func(black_box(&format!("../input/real/{}", day))))
        });
    }
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);
