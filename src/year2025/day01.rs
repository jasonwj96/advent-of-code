use std::fs::File;
use std::io::{self, BufRead, BufReader};
use std::path::Path;

pub fn parse<P: AsRef<Path>>(path: P) -> io::Result<Vec<(char, i32)>> {
    let file = File::open(path)?;
    let reader = BufReader::new(file);
    let mut result: Vec<(char, i32)> = Vec::new();

    for line in reader.lines() {
        let line = line?;
        let line = line.trim();

        let mut chars = line.chars();
        let dir = chars.next().unwrap();
        let value: i32 = chars.as_str().parse().unwrap();

        result.push((dir, value));
    }

    Ok(result)
}

pub fn part1(input: &[(char, i32)]) -> u32 {
    let mut dial: i32 = 50;
    let mut result = 0;

    for &(dir, steps) in input {
        let steps = steps as i32;

        dial += match dir {
            'R' => steps,
            'L' => -steps,
            _ => 0,
        };

        if dial.rem_euclid(100) == 0 {
            result += 1;
        }
    }

    result
}

pub fn part2(input: &[(char, i32)]) -> i32 {
    let mut dial: i32 = 50;
    let mut result: i32 = 0;

    for &(dir, steps) in input {
        match dir {
            'R' => {
                result += (dial + steps) / 100;
                dial = (dial + steps) % 100;
            }
            'L' => {
                let reversed = (100 - dial) % 100;
                result += (reversed + steps) / 100;
                dial = (dial - steps).rem_euclid(100);
            }
            _ => {}
        }
    }

    result
}