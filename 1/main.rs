fn main() {

    let input: String = std::fs::read_to_string("input.txt").expect("");
    let input_lines: Vec<&str> = input.split("\n").collect::<Vec<&str>>();

    let mut first: char;
    let mut last: char;
    let mut numbers: Vec<u32> = Vec::new();
    
    // P1
    for line in &input_lines {
        if line.len() == 0 {continue;}
        first = '\0';
        last = '\0';

        for c in line.chars().collect::<Vec<char>>() {
            if (c as u8) >= 48 && (c as u8) <= 57 {
                if first == '\0' {first = c};
                last = c;
            }
        }
        
        let mut number: String = String::new();
        number.push(first);
        number.push(last);

        numbers.push(number.parse::<u32>().unwrap());
    }

    let part_1 = numbers.iter().sum::<u32>();
    println!("P1 {}", part_1);    
    
    // P2
    numbers.clear();
    for line in &input_lines {
        if line.len() == 0 {continue;}
        first = '\0';
        last = '\0';
        
        for (i, c) in line.chars().collect::<Vec<char>>().iter().enumerate() {
            let digit = match c {
                '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' => c,
                'o' => {
                    if line[i..].starts_with("one") {&'1'}
                    else {&'\0'}
                },
                't' => {
                    if line[i..].starts_with("two") {&'2'}
                    else if line[i..].starts_with("three") {&'3'}
                    else {&'\0'}
                },
                'f' => {
                    if line[i..].starts_with("four") {&'4'}
                    else if line[i..].starts_with("five") {&'5'}
                    else {&'\0'}},
                's' => {
                    if line[i..].starts_with("six") {&'6'}
                    else if line[i..].starts_with("seven") {&'7'}
                    else {&'\0'}},
                'e' => {
                    if line[i..].starts_with("eight") {&'8'}
                    else {&'\0'}
                },
                'n' => {
                    if line[i..].starts_with("nine") {&'9'}
                    else {&'\0'}
                },
                _ => &'\0'
            };

            if first == '\0' {first = *digit;}
            if *digit != '\0' {last = *digit;}
        }

        let mut number: String = String::new();
        number.push(first);
        number.push(last);

        numbers.push(number.parse::<u32>().unwrap());
    }

    let part_2 = numbers.iter().sum::<u32>();
    println!("P2 {}", part_2);
}