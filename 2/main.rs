fn main() {

    let max_red = 12;
    let max_green = 13;
    let max_blue = 14;

    let input: String = std::fs::read_to_string("input.txt").expect("");
    let input_lines: Vec<&str> = input.split("\n").collect::<Vec<&str>>();

    let mut p1: u32 = 0; 
    let mut p2: u32 = 0; 

    for line in input_lines {
        if line.len() == 0 {continue;}
        // Split into [id, rounds]
        let game_info: Vec<&str> = line.split(": ").collect::<Vec<&str>>();
    
        // Extract id and check if any balls are too high 
        let id = game_info[0][5..].parse::<u32>().unwrap();

        // Extract data from each round
        let rounds = game_info[1].split("; ").collect::<Vec<&str>>();
        let mut possible = true;
        let mut min_red = 0;
        let mut min_green = 0;
        let mut min_blue = 0;
        // Iterate over all "rounds" from each "game" and not whether it is possible or not
        for round in rounds {
            let rgb = round.split(", ").collect::<Vec<&str>>();

            for pull in rgb {
                if pull.ends_with("red") {
                    let amount = pull[0..pull.len()-4].parse::<u32>().unwrap();
                    if amount > max_red {possible = false};
                    if amount > min_red {min_red = amount};
                }
                else if pull.ends_with("green") {
                    let amount = pull[0..pull.len()-6].parse::<u32>().unwrap();
                    if amount > max_green {possible = false};
                    if amount > min_green {min_green = amount};
                }
                else if pull.ends_with("blue") {
                    let amount = pull[0..pull.len()-5].parse::<u32>().unwrap();
                    if amount > max_blue {possible = false};
                    if amount > min_blue {min_blue = amount};
                }
            }

        }
        if possible {p1 += id;}
        let power = min_red * min_green * min_blue;
        p2 += power;
    }

    println!("P1 {}", p1);
    println!("P1 {}", p2);

}