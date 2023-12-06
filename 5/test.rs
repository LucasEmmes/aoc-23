use std::ops::RangeInclusive;
use std::collections::HashMap;

fn overlap(r1: &RangeInclusive<i64>, r2: &RangeInclusive<i64>) -> Option<RangeInclusive<i64>> {
    let start = std::cmp::max(r1.start(), r2.start());
    let end = std::cmp::max(r1.end(), r2.end());
    if start <= end {return Some(*start..=*end);}
    else {return None}
}

fn main() {
    let input: String = std::fs::read_to_string("input.txt").expect("");
    let input_lines: Vec<&str> = input.split("\n").filter(|x| x.len() > 0).collect();

    let map_names = ["seed-to-soil map:", "soil-to-fertilizer map:", "fertilizer-to-water map:", "water-to-light map:", "light-to-temperature map:", "temperature-to-humidity map:", "humidity-to-location map:"];

    let raw_seeds = input_lines[0].split(": ").collect::<Vec<&str>>()[1].split(" ").map(|x| x.parse::<i64>().unwrap()).collect::<Vec<i64>>();
    let mut seeds: Vec<RangeInclusive<i64>> = Vec::new();
    for i in (0..raw_seeds.len()).step_by(2) {
        seeds.push(raw_seeds[i]..=raw_seeds[i+1]);
    }

    let mut inital_map: HashMap<&str, Vec<Vec<RangeInclusive<i64>>>> = HashMap::new();
    let mut current_map: &mut Vec<Vec<RangeInclusive<i64>>> = &mut Vec::new();

    for line in &input_lines[1..] {
        if line.contains("map") {
            inital_map.insert(line, Vec::new());
            current_map = inital_map.get_mut(line).unwrap();
        }
        else {
            let (from, to) = destructure(*line);
            current_map.push(vec![from, to]);
        }
    }

    let mut p1 = i64::MAX;

    for seed in &seeds {
        let mut a = *seed.start();
        let mut b = *seed.end();
        for map_name in &map_names {
            a = translate(inital_map.get(map_name).unwrap(), a, true);
            b = translate(inital_map.get(map_name).unwrap(), b, true);
        }

        if a < p1 {p1 = a};
        if b < p1 {p1 = b};
    }

    println!("P1 {}", p1);

    for map_name in &map_names {
        let mut map = inital_map.get_mut(map_name).unwrap();
        map.sort_by_key(|x| *x[0].start());
        let start_len = map.len();
        
        // Add first
        if *map[0][0].start() > 0 {
            map.push(vec![0..=*map[0][0].start()-1, 0..=*map[0][0].start()-1]);
        }

        // Add last
        if *map.last().unwrap()[0].end() < i64::MAX {
            map.push(vec![*map.last().unwrap()[0].end()+1..=i64::MAX, *map.last().unwrap()[0].end()+1..=i64::MAX]);
        }

        // Add inbetweens
        for i in 0..start_len-1 {
            let delta = *map[i+1][0].start() - *map[i][0].end() - 1;
            if delta > 0 {
                map.push(vec![*map[i][0].end()+1..=*map[i][0].end()+1+delta, *map[i][0].end()+1..=*map[i][0].end()+1+delta]);
            }
        }

        map.sort_by_key(|x| *x[0].start());
    }
}

fn destructure(line: &str) -> (RangeInclusive<i64>, RangeInclusive<i64>) {
    let data = line.split(" ").map(|x| x.parse::<i64>().unwrap()).collect::<Vec<i64>>();
    let destination = data[0];
    let source = data[1];
    let range = data[2];

    return (source..=source+range-1, destination..=destination+range-1);
}

fn translate(table: &Vec<Vec<RangeInclusive<i64>>>, value: i64, forward: bool) -> i64 {
    for entry in table {
        if forward {
            if entry[0].contains(&value) {
                let delta = entry[1].start() - entry[0].start();
                return value+delta;
            }
        } else {
            if entry[1].contains(&value) {
                let delta = entry[1].start() - entry[0].start();
                return value-delta;
            }
        }
    }
    
    return value;
}