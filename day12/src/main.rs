fn main() {
    let input: String = std::fs::read_to_string("demo.txt").expect("");
    let lines: Vec<&str> = input.split("\n").filter(|x| !x.is_empty()).collect::<Vec<&str>>();

    // let mut p1 = 0;
    // let mut p2 = 0;
    for (i, line) in lines.clone().into_iter().enumerate() {
        // Common
        let data = line.split(" ").collect::<Vec<&str>>();
        let segment_str = data[0];
        let values_str = data[1];

        // P1 setup
        let values = values_str.split(",").map(|x| x.parse::<i64>().unwrap()).collect::<Vec<i64>>();
        let total_chars: i64 = segment_str.len() as i64;
        let total_values = values.clone().into_iter().reduce(|a, b| a+b).unwrap() + values.len() as i64 - 1;
        let number_of_periods = total_chars - total_values;
        // P1 check
        let perms = create_perms(number_of_periods, values.len() as i64 + 1, 0);
        for perm in perms {
            let masked = apply_mask(&values, &perm);
            if check_match(segment_str, &masked) {
                // p1 += 1;
            }
        }

        // P2 setup
        let segment_str_p2 = segment_str;
        let values_str_p2  = values_str;
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

        // P2 check
        println!("{} possible perms", get_perm_count(number_of_periods, values.len() as i64+1));
        println!("{} possible board", 2i64.pow(segment_str_p2.matches('?').count() as u32));
        println!();
        // let perms = create_perms(number_of_periods, values.len() as i64 + 1, 0);
        // for perm in perms {
        //     let masked = apply_mask(&values, &perm);
        //     if check_match(&segment_str_p2, &masked) {
        //         p1 += 1;
        //     }
        // }
    }

    // println!("P1 {p1}");
    // println!("P2 {p2}");

}

fn check_match(segment_str: &str, verification: &str) -> bool {
    let seg_vec = segment_str.chars().collect::<Vec<char>>();
    let ver_vec = verification.chars().collect::<Vec<char>>();
    for i in 0..segment_str.len() {
        if seg_vec[i] != '?' && seg_vec[i] != ver_vec[i] {
            return false;
        }
    }
    return true;
}

fn make_segment(length: i64, period: bool, is_end: bool) -> String {
    let mut res = String::new();
    if period {
        for i in 0..length {res.push('.');}
        return res;
    }
    else {
        for i in 0..length {res.push('#');}
        if !is_end {res.push('.');}
        return res;
    }
}

fn apply_mask(values: &Vec<i64>, perm: &Vec<i64>) -> String {
    let mut res: String = String::new();
    res.push_str(&make_segment(*perm.first().unwrap(), true, false));

    for i in 0..values.len()-1 {
        res.push_str(&make_segment(values[i], false, false));
        res.push_str(&make_segment(perm[i+1], true, false));
    }
    res.push_str(&make_segment(*values.last().unwrap(), false, true));
    res.push_str(&make_segment(*perm.last().unwrap(), true, false));
    return res;
}

fn create_perms(periods_left: i64, spaces_left: i64, min: i64) -> Vec<Vec<i64>> {
    if spaces_left == 1 {
        return vec![vec![periods_left]];
    }
    let mut i: i64 = periods_left;
    let mut res: Vec<Vec<i64>> = Vec::new();
    while i >= min {
        for mut v in create_perms(periods_left-i, spaces_left-1, 0) {
            let mut temp: Vec<i64> = vec![i];
            temp.append(&mut v);
            res.push(temp);
        }
        i -= 1;
    }
    return res;
}

fn get_perm_count(periods: i64, slots: i64) -> i64 {
    return binomial_coefficient(periods+slots-1, slots-1);
}

fn binomial_coefficient(n: i64, m: i64) -> i64 {
    let mut res = 1;
 
    let mut m = m;
    if (m > n - m) {
        m = n - m;
    }

    let mut i = 0;
    while i < m {
        res *= (n - i);
        res /= (i + 1);
        i += 1;
    }
 
    return res;
}