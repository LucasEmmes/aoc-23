use std::collections::HashMap;

fn main() {
    let input: String = std::fs::read_to_string("input.txt").expect("");
    let input_lines: Vec<&str> = input.split("\n").filter(|x| x.len() > 0).collect();

    let seeds = input_lines[0].split(": ").collect::<Vec<&str>>()[1].split(" ").map(|x| x.parse::<u64>().unwrap()).collect::<Vec<u64>>();
    
    let map_names = ["seed-to-soil map:", "soil-to-fertilizer map:", "fertilizer-to-water map:", "water-to-light map:", "light-to-temperature map:", "temperature-to-humidity map:", "humidity-to-location map:"];
    let mut big_map: HashMap<&str, HashMap<u64, (u64, u64)>> = HashMap::new();
    for map_name in map_names {big_map.insert(map_name, HashMap::new());}

    let mut current_map: &mut HashMap<u64, (u64, u64)> = &mut HashMap::new();


    for line in &input_lines[1..] {
        if line.contains("map") {
            current_map = big_map.get_mut(*line).unwrap();
        }
        else {
            let (source, destination, range) = destructure(*line);
            current_map.insert(source, (destination, range));
        }
    }

    let mut lowest_location = u64::MAX;
    
    for seed in &seeds {        
        let mut temp: u64 = *seed;
        for map_name in map_names {
            temp = translate(big_map.get(map_name).unwrap(), temp);
        }
        if temp < lowest_location {
            lowest_location = temp;
        }
    }
    
    println!("P1 {}", lowest_location);

    lowest_location = u64::MAX;
    for i in (0..seeds.len()).step_by(2) {
        for j in 0..seeds[i+1] {
            let mut temp: u64 = seeds[i]+j;
            for map_name in map_names {
                temp = translate(big_map.get(map_name).unwrap(), temp);
            }
            if temp < lowest_location {
                lowest_location = temp;
            }
        }
    }

    println!("P2 {}", lowest_location);
}


fn destructure(line: &str) -> (u64, u64, u64) {
    let data = line.split(" ").map(|x| x.parse::<u64>().unwrap()).collect::<Vec<u64>>();
    let destination = data[0];
    let source = data[1];
    let range = data[2];

    return (source, destination, range);
}

fn translate(map: &HashMap<u64, (u64, u64)>, source: u64) -> u64 {
    let mut keys = map.keys().collect::<Vec<&u64>>();
    keys.sort();
    
    for key in keys {
        if key <= &source {
            let (target, range) = map.get(key).unwrap();
            if (key + range) >= source {
                let result = target + source - key;
                return result;
            }
        }
    }

    return source;
}