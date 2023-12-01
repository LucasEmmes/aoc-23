fn main() {

    let input: String = std::fs::read_to_string("input.txt").expect("");
    let input_lines: Vec<&str> = input.split("\n").collect::<Vec<&str>>();

    let mut first: char;
    let mut last: char;
    let mut numbers: Vec<u32> = Vec::new();
        first = '_';
        last = '_';

    for line in &input_lines {
        if line.len() == 0 {continue;}

        let mut line_as_chars = line.chars().collect::<Vec<char>>();

        for c in &line_as_chars {
            if (*c as u8) >= 48 && (*c as u8) <= 57 {
                first = *c;
                break;
            }
        }
        
        line_as_chars.reverse();
        
        for c in &line_as_chars {
            if (*c as u8) >= 48 && (*c as u8) <= 57 {
                last = *c;
                break;
            }
        }
        
        let mut number: String = String::new();
        if (first != '_') {number.push(first);}
        if (last != '_') {number.push(last);}

        numbers.push(number.parse::<u32>().unwrap());
    }

    let part_1 = numbers.iter().sum::<u32>();
    println!("{}", part_1);    
    numbers.clear();


    for line in &input_lines {
        first = '_';
        last = '_';
        if line.len() == 0 {continue;}
        
        for (i, c) in line.chars().collect::<Vec<char>>().iter().enumerate() {
            let digit = match c {
                '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' => c,
                'o' => {if line[i..].starts_with("one") {&'1'} else {&'_'}},
                't' => {
                    if line[i..].starts_with("two") {&'2'}
                    else if line[i..].starts_with("three") {&'3'}
                    else {&'_'}
                },
                'f' => {
                    if line[i..].starts_with("four") {&'4'}
                    else if line[i..].starts_with("five") {&'5'}
                    else {&'_'}},
                's' => {
                    if line[i..].starts_with("six") {&'6'}
                    else if line[i..].starts_with("seven") {&'7'}
                    else {&'_'}},
                'e' => {if line[i..].starts_with("eight") {&'8'} else {&'_'}},
                'n' => {if line[i..].starts_with("nine") {&'9'} else {&'_'}},
                _ => &'_'
            };

            // println!("\nDigit: {}", digit);

            if digit != &'_' {
                if first == '_' {
                    // println!("Set first");
                    first = *digit;
                }
                    // println!("Set last");
                last = *digit;
            }
        }

        let mut number: String = String::new();
        if (first != '_') {number.push(first);}
        if (last != '_') {number.push(last);}

        println!("{}", number);    
        numbers.push(number.parse::<u32>().unwrap());
    }

    let part_2 = numbers.iter().sum::<u32>();
    println!("{}", part_2);  
}