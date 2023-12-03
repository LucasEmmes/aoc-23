fn main() {
    use std::collections::VecDeque;
    use std::collections::HashMap;

    let input: String = std::fs::read_to_string("input.txt").expect("");
    let mut input_lines: VecDeque<String> = input.split("\n").map(|x| String::from(".") + x + ".").collect::<VecDeque<String>>();
    if input_lines.back().expect("").len() == 2 {input_lines.pop_back();} // Remove that empty line

    // Prepping to make sure no number will touch any of the map's edges
    let line_length = input_lines[0].len();
    let mut empty_line = String::new();
    for _ in 0..line_length {empty_line.push('.');}
    input_lines.push_front(empty_line.clone());
    input_lines.push_back(empty_line.clone());

    let mut p1: u32 = 0;

    let mut gears: HashMap<(i32, i32), Vec<u32>> = HashMap::new();

    // Extraction time
    for line_num in 0..input_lines.len() {
        let mut start: i32 = -1;
        let mut end: i32 = -1;
        let mut number: String = String::new();
        let line = &input_lines[line_num];

        for (i, c) in line.chars().enumerate() {
            match c {
                '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9' => {
                    // Note new start and end points
                    if start == -1 {start = i as i32;}
                    end = i as i32;
                    number.push(c);
                },
                _ => {
                    // If the last chars have been periods, just do nothing
                    if start == -1 {continue;}
                    // If it is first one we see after reading a number, do a surroundings-check
                    let mut is_partnumber: bool = false;
                    for y in line_num-1..=line_num+1 {
                        for x in start-1..=end+1 {
                            let touching_char = input_lines[y].chars().collect::<Vec<char>>()[x as usize];
                            // print!("{}", touching_char);
                            match touching_char {
                                '0'|'1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'|'.' => (),
                                '*' => {
                                    is_partnumber = true;
                                    if !gears.contains_key(&(x, y as i32)) {
                                        gears.insert((x, y as i32), Vec::new());
                                    }
                                    gears.get_mut(&(x, y as i32)).expect("").push(number.parse::<u32>().unwrap());
                                },
                                _ => is_partnumber = true // If it is anything but a number or period, it is a symbol
                            }
                        }
                    }

                    if is_partnumber {p1 += number.parse::<u32>().unwrap();}
                    number.clear();
                    start = -1;
                    end = -1;
                }
            }
        }
    }

    println!("P1 {}", p1);
    
    let mut p2: u32 = 0;
    for values in gears.into_values() {
        if values.len() == 2 {
            p2 += values[0]*values[1];
        }
    }

    println!("P2 {}", p2);

}