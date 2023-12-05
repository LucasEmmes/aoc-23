use std::collections::HashMap;

fn main() {


    let input: String = std::fs::read_to_string("input.txt").expect("");
    let input_lines: Vec<&str> = input.split("\n").collect::<Vec<&str>>();
    // if input_lines.last().unwrap().len() == 0 {input_lines.pop();}

    let seeds = input_lines[0].split(": ").collect::<Vec<&str>>()[1].split(" ").map(|x| x.parse::<u64>().unwrap()).collect::<Vec<u64>>();
    println!("{:?}", seeds);
    
    let mut seed_to_soil: HashMap<u64, (u64, u64)> = HashMap::new();
    let mut soil_to_fertilizer: HashMap<u64, (u64, u64)> = HashMap::new();
    let mut fertilizer_to_water: HashMap<u64, (u64, u64)> = HashMap::new();
    let mut water_to_light: HashMap<u64, (u64, u64)> = HashMap::new();
    let mut light_to_temperature: HashMap<u64, (u64, u64)> = HashMap::new();
    let mut temperature_to_humidity: HashMap<u64, (u64, u64)> = HashMap::new();
    let mut humidity_to_location: HashMap<u64, (u64, u64)> = HashMap::new();

    let mut it = 2;
    while it < input_lines.len() {
        let line = input_lines[it];
        
        // Extract
        if line == "seed-to-soil map:" {
            it+=1;
            let line = input_lines[it];
            while line != "" {
                let (source, destination, range) = destructure(line);
                seed_to_soil.insert(source, (destination, range));
            }
        }

        if line == "soil-to-fertilizer map:" {
            it+=1;
            let line = input_lines[it];
            while line != "" {
                let (source, destination, range) = destructure(line);
                soil_to_fertilizer.insert(source, (destination, range));
            }
        }
        
        if line == "fertilizer-to-water map:" {
            it+=1;
            let line = input_lines[it];
            while line != "" {
                let (source, destination, range) = destructure(line);
                fertilizer_to_water.insert(source, (destination, range));
            }
        }

        if line == "water-to-light map:" {
            it+=1;
            let line = input_lines[it];
            while line != "" {
                let (source, destination, range) = destructure(line);
                water_to_light.insert(source, (destination, range));
            }
        }

        if line == "light-to-temperature map:" {
            it+=1;
            let line = input_lines[it];
            while line != "" {
                let (source, destination, range) = destructure(line);
                light_to_temperature.insert(source, (destination, range));
            }
        }

        if line == "temperature-to-humidity map:" {
            it+=1;
            let line = input_lines[it];
            while line != "" {
                let (source, destination, range) = destructure(line);
                temperature_to_humidity.insert(source, (destination, range));
            }
        }

        if line == "humidity-to-location map:" {
            it+=1;
            let line = input_lines[it];
            while line != "" {
                let (source, destination, range) = destructure(line);
                humidity_to_location.insert(source, (destination, range));
            }
        }
    }

    let mut lowest_seed = u64::MAX;
    let mut lowest_location = u64::MAX;

    for seed in seeds {
        
    }

}


fn destructure(line: &str) -> (u64, u64, u64) {
    let data = line.split(" ").map(|x| x.parse::<u64>().unwrap()).collect::<Vec<u64>>();
    let destination = data[0];
    let source = data[1];
    let range = data[2];

    return (source, destination, range);
}

fn translate(map: &HashMap<u64, (u64, u64)>, source: u64) -> u64 {
    let mut keys = map.keys().collect::<Vec<u64>>();
    keys.sort();
    // for key in 
    return 1;
}