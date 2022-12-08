use std::env;
use std::fs::File;
use std::io::prelude::*;


fn main() {
    let args: Vec<String> = env::args().collect();

    let filename = &args[1];
    let mut f = File::open(filename).expect("Cannot open file");
    let mut contents = String::new();
    f.read_to_string(&mut contents).expect("Cannot read file");

    let mut calorie_counts = contents.lines();
    let mut top_calories: Vec<i32> = vec![0, 0, 0];
    let mut cur_calories: i32 = 0;
    loop {
      match calorie_counts.next() {
        None => { break; }
        Some("") => {
            let pos = top_calories.binary_search(&cur_calories).unwrap_or_else(|e| e);
            top_calories.insert(pos, cur_calories);
            top_calories.remove(0);
            cur_calories = 0;
        },
        Some(calorie_value) => {
            let calorie_value_as_int : i32 = calorie_value.parse().unwrap();
            cur_calories += calorie_value_as_int;
        }
      }
    }
    let pos = top_calories.binary_search(&cur_calories).unwrap_or_else(|e| e);
    top_calories.insert(pos, cur_calories);
    top_calories.remove(0);
    println!("{:?}", top_calories.iter().sum::<i32>());
}