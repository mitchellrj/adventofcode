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
    let mut max_calories = 0;
    let mut cur_calories = 0;
    loop {
      match calorie_counts.next() {
        None => { break; }
        Some("") => {
            if cur_calories > max_calories {
                max_calories = cur_calories;
            }
            cur_calories = 0;
        },
        Some(calorie_value) => {
            let calorie_value_as_int : i32 = calorie_value.parse().unwrap();
            cur_calories += calorie_value_as_int;
        }
      }
    }
    if cur_calories > max_calories {
        max_calories = cur_calories;
    }
    println!("{:?}", max_calories)
}