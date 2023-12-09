fn main() {
    use std::collections::HashMap;
    use std::collections::HashSet;

    let input: String = std::fs::read_to_string("input.txt").expect("");
    let input_lines: Vec<&str> = input.split('\n').filter(|x| !x.is_empty()).collect::<Vec<&str>>();

    let directions = input_lines[0].chars().collect::<Vec<char>>();

    let mut nodes: HashMap<&str, (&str, &str)> = HashMap::new();

    for line in &input_lines[1..] {
        // "RBX = (TMF, KTP)" => ["RBX", "=", "(TMF,", "KTP)"]
        let names = line.split(" ").collect::<Vec<&str>>();
        // Get names
        let name_from = &names[0];
        let name_left = &names[2][1..names[2].len()-1];
        let name_right = &names[3][..names[3].len()-1];
        nodes.insert(&name_from, (name_left, name_right));
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

    
    let mut steps: HashMap<&str, HashSet<(&str, u64)>> = HashMap::new();
    let mut starts: Vec<&str> = Vec::new();    

    // while !done(&currents) {
    //     let lr = directions[counter % directions.len()];
    //     for i in 0..currents.len() {
    //         let mut current = currents[i];
    //         if let Some(next_node) = nodes.get(current) {
    //             if lr == 'L' {
    //                 current = next_node.0;
    //             } else if lr == 'R' {
    //                 current = next_node.1;
    //             }
    //         }
    //         currents[i] = current;
    //     }
    //     counter += 1;
    // }

    // println!("P2 {}", counter_p2);

}

// fn done(currents: &Vec<&str>) -> bool {
//     let mut all_end = true;
//         for current in currents {
//         all_end &= current.ends_with("Z");
//     }
//     return all_end;
// }