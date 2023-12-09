fn main() {
    let input: String = std::fs::read_to_string("input.txt").expect("");
    let input_lines: Vec<&str> = input.split("\n").filter(|x| !x.is_empty()).collect::<Vec<&str>>();

    let mut p1 = 0;
    let mut p2 = 0;
    for line in input_lines {
        let sequence = line.split(" ").map(|x| x.parse::<i64>().unwrap()).collect::<Vec<i64>>();
        p1 += reduce_p1(&sequence);
        p2 += reduce_p2(&sequence);
    }

    println!("P1 {}", p1);
    println!("P2 {}", p2);
}

fn reduce_p1(sequece: &Vec<i64>) -> i64 {
    let mut bottom = true;
    for v in sequece {bottom &= *v == 0}
    if bottom {return 0;}

    let mut reduced = Vec::new();
    for i in 0..sequece.len()-1 {
        reduced.push(sequece[i+1]-sequece[i]);
    }
    return sequece.last().unwrap() + reduce_p1(&reduced);
}

fn reduce_p2(sequece: &Vec<i64>) -> i64 {
    let mut bottom = true;
    for v in sequece {bottom &= *v == 0}
    if bottom {return 0;}

    let mut reduced = Vec::new();
    for i in 0..sequece.len()-1 {
        reduced.push(sequece[i+1]-sequece[i]);
    }
    return sequece.first().unwrap() - reduce_p2(&reduced);
}