fn main() {
    use std::collections::HashMap;
    use std::collections::HashSet;

    let input: String = std::fs::read_to_string("input.txt").expect("");
    let input_lines: Vec<&str> = input.split('\n').filter(|x| !x.is_empty()).collect::<Vec<&str>>();

    let directions = input_lines[0].chars().collect::<Vec<char>>();

    let mut nodes: HashMap<&str, (&str, &str)> = HashMap::new();
    let mut starts: Vec<&str> = Vec::new();

    for line in &input_lines[1..] {
        // "RBX = (TMF, KTP)" => ["RBX", "=", "(TMF,", "KTP)"]
        let names = line.split(" ").collect::<Vec<&str>>();
        // Get names
        let name_from = &names[0];
        let name_left = &names[2][1..names[2].len()-1];
        let name_right = &names[3][..names[3].len()-1];
        nodes.insert(&name_from, (name_left, name_right));
        if name_from.ends_with("A") {
            starts.push(&name_from);
        }
    }

    
    let mut current = "AAA";
    let mut counter_p1 = 0;
    while current != "ZZZ" {
        let lr = directions[counter_p1 % directions.len()];
        if let Some(next_node) = nodes.get(current) {
            if lr == 'L' {
                current = next_node.0;
            } else if lr == 'R' {
                current = next_node.1;
            }
            counter_p1 += 1;
        }
    }
    println!("P1 {}", counter_p1);

    
    let mut cycle_times: Vec<i64> = Vec::new();

    for start in starts {
        let mut current = start;
        let mut seen: HashSet<(&str, i64)> = HashSet::new();
        let mut counter: usize = 0;

        loop {
            seen.insert((current, (counter%directions.len()) as i64));
            let next_node = nodes.get(current).unwrap();
            if directions[counter%directions.len()] == 'L' {
                current = next_node.0;
            } else {
                current = next_node.1;
            }
            counter += 1;

            if current.ends_with("Z") {
                cycle_times.push(counter as i64);
                break;
            }
        }
    }

    let gcd = &cycle_times.clone().into_iter().reduce(|a, b| GCD(a, b)).unwrap();

    let mut reduced_cycles = Vec::new();
    for cycle in &cycle_times {
        reduced_cycles.push(cycle / gcd);
    }

    let p2 = &reduced_cycles.clone().into_iter().reduce(|a, b| a*b).unwrap() * gcd;
    println!("P2 {p2}");

}

fn GCD(a: i64, b: i64) -> i64 {
    if b == 0 {return a;}
    return GCD(b, a%b);
}