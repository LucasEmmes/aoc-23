use std::collections::HashMap;
fn main() {
    let now = std::time::Instant::now();

    let input: String = std::fs::read_to_string("input.txt").expect("");
    let lines: Vec<&str> = input.split("\n").filter(|x| !x.is_empty()).collect::<Vec<&str>>();
    
    let mut p1 = 0;
    let mut p2 = 0;
    for (_, line) in lines.clone().into_iter().enumerate() {
        let mut memo: HashMap<(i64, i64, i64), i64> = HashMap::new();
        // Common
        let data = line.split(" ").collect::<Vec<&str>>();
        let segment_str = data[0];
        let values_str = data[1];

        // P1
        let values = values_str.split(",").map(|x| x.parse::<i64>().unwrap()).collect::<Vec<i64>>();
        let total_chars: i64 = segment_str.len() as i64;
        let total_mandatory_chars = values.clone().into_iter().reduce(|a, b| a+b).unwrap() + values.len() as i64 - 1;
        let number_of_periods = total_chars - total_mandatory_chars;
        let mandatory: Vec<String> = make_mandatory(&values);
        p1 += solve(number_of_periods, &mandatory, segment_str, &mut memo);

        // P2
        let mut segment_str_p2 = String::new();
        let mut values_str_p2  = String::new();
        for _ in 0..4 {
            segment_str_p2.push_str(&segment_str);
            segment_str_p2.push('?');
            values_str_p2.push_str(&values_str);
            values_str_p2.push(',');
        }
        segment_str_p2.push_str(&segment_str);
        values_str_p2.push_str(&values_str);
        let values = values_str_p2.split(",").map(|x| x.parse::<i64>().unwrap()).collect::<Vec<i64>>();
        let total_chars: i64 = segment_str_p2.len() as i64;
        let total_values = values.clone().into_iter().reduce(|a, b| a+b).unwrap() + values.len() as i64 - 1;
        let number_of_periods = total_chars - total_values;
        let mandatory: Vec<String> = make_mandatory(&values);
        p2 += solve(number_of_periods, &mandatory, &segment_str_p2, &mut memo);
    }

    println!("P1 {p1}");
    println!("P2 {p2}");

    println!("Elapsed: {:.2?}", now.elapsed());
}

fn solve(periods_left: i64, mandatory_left: &[String], segment_left: &str, memo: &mut HashMap<(i64, i64, i64), i64>) -> i64 {
    if periods_left == 0 && mandatory_left.len() == 0 && segment_left.len() == 0 {return 1;}
    
    let key = (periods_left, mandatory_left.len() as i64, segment_left.len() as i64);
    if memo.contains_key(&key) {
        return *memo.get(&key).unwrap();
    }

    let mut res = 0;

    // Check if we can add a period
    if periods_left > 0 && can_hold(segment_left, &".") {
        res += solve(periods_left-1, mandatory_left, &segment_left[1..], memo);
    }

    if mandatory_left.len() > 0 && can_hold(segment_left, mandatory_left.first().unwrap()) {
        res += solve(periods_left, &mandatory_left[1..], &segment_left[mandatory_left.first().unwrap().len()..], memo)
    }

    memo.insert(key, res);

    return res;
}

fn can_hold(segment: &str, mandatory: &str) -> bool {
    if segment.len() < mandatory.len() {return false;}

    let seg_chars = segment.chars().collect::<Vec<char>>();
    let man_chars = mandatory.chars().collect::<Vec<char>>();
    
    for i in 0..man_chars.len() {
        if seg_chars[i] != '?' && seg_chars[i] != man_chars[i] {
            return false;
        }
    }
    return true;
}

fn make_mandatory(values: &Vec<i64>) -> Vec<String> {
    let mut mandatory: Vec<String> = Vec::new();
    for value in &values[..values.len()-1] {
        mandatory.push(make_segment(*value, true));
    }
    mandatory.push(make_segment(*values.last().unwrap(), false));
    return mandatory;
}

fn make_segment(length: i64, period: bool) -> String {
    let mut res = String::new();
    for _ in 0..length {res.push('#');}
    if period {res.push('.');}
    return res;
}