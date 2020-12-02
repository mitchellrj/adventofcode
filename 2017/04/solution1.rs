use std::fs::File;
use std::collections::HashMap;
use std::io::prelude::*;


fn main() {
    let filename = "passphrases.txt";
    let mut f = File::open(filename).expect("Cannot open file");
    let mut contents = String::new();
    f.read_to_string(&mut contents).expect("Cannot read file");

    let mut phrases = contents.lines();
    let mut phrase_count = 0;
    let mut invalid_count = 0;
    loop {
      match phrases.next() {
        None => { break },
        Some(phrase) => {
          phrase_count += 1;
          let mut words = phrase.split_whitespace();
          let mut unique_words = HashMap::new();
          loop {
            match words.next() {
              None => { break },
              Some(word) => {
                if unique_words.insert(word, true) != None {
                  invalid_count += 1;
                  break;
                }
              }
            }
          }
        }
      }
    }
    println!("{:?}", phrase_count - invalid_count)
}