fn main() {
    use std::collections::HashMap;

    let input: String = std::fs::read_to_string("input.txt").expect("");
    let input_lines: Vec<&str> = input.split("\n").collect::<Vec<&str>>();

    // Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    let mut p1: i32 = 0;
    
    let mut scratchcards_winnings: HashMap<i32, i32> = HashMap::new();

    for line in input_lines {
        if line.len() == 0 {continue;}

        let line = line.split(": ").collect::<Vec<&str>>()[1];
        let parts = line.split(" | ").collect::<Vec<&str>>();
        let winning = parts[0].split(" ").filter(|x| x.len() > 0).collect::<Vec<&str>>();
        let gotten = parts[1].split(" ").filter(|x| x.len() > 0).collect::<Vec<&str>>();

        let mut card_score = 0;
        for num in gotten {
            if winning.contains(&num) {
                if card_score == 0 {card_score = 1;}
                else {card_score *= 2;}
            }
        }

        p1 += card_score;
    }

    println!("P1 {}", p1);

}