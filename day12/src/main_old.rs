use core::num;

fn main() {
    let input: String = std::fs::read_to_string("demo.txt").expect("");
    let lines: Vec<&str> = input.split("\n").filter(|x| !x.is_empty()).collect::<Vec<&str>>();

    let mut p1 = 0;
    let mut p2 = 0;
    for (i, line) in lines.clone().into_iter().enumerate() {
        // Common
        let data = line.split(" ").collect::<Vec<&str>>();
        let segment_str = data[0];
        let values_str = data[1];

        // P1
        // let values = values_str.split(",").map(|x| x.parse::<i64>().unwrap()).collect::<Vec<i64>>();
        // let total_chars: i64 = segment_str.len() as i64;
        // let total_values = values.clone().into_iter().reduce(|a, b| a+b).unwrap();
        // let number_of_periods = total_chars - total_values;
        
        // let perms = create_perms(number_of_periods, values.len() as i64 + 1, 0);
        // for perm in perms {
        //     let masked = &apply_mask(&values, &perm)[..];
        //     if check_match(segment_str, masked) {
        //         p1 += 1;
        //     }
        // }

        // P2
        let segment_str_p2 = segment_str;
        let values_str_p2  = values_str;
        // let mut segment_str_p2 = String::new();
        // let mut values_str_p2  = String::new();
        // for _ in 0..4 {
        //     segment_str_p2.push_str(&segment_str);
        //     segment_str_p2.push('?');
        //     values_str_p2.push_str(&values_str);
        //     values_str_p2.push(',');
        // }
        // segment_str_p2.push_str(&segment_str);
        // values_str_p2.push_str(&values_str);
        
        let values = values_str_p2.split(",").map(|x| x.parse::<i64>().unwrap()).collect::<Vec<i64>>();
        let total_chars: i64 = segment_str_p2.len() as i64;
        let total_values = values.clone().into_iter().reduce(|a, b| a+b).unwrap();
        let number_of_periods = total_chars - total_values;
        
        p2 += get_matches(number_of_periods, values_str_p2, segment_str_p2, false);
    }

    // println!("P1 {p1}");
    println!("P2 {p2}");

}

fn get_matches(periods_left: i64, values_left: &str, segments_left: &str, must_be_period: bool) -> i64 {
    if periods_left < values_left.len() as i64 - 1 {return 0;}
    else if periods_left < values_left.len() as i64 && must_be_period == true {return 0;}
    else if segments_left.is_empty() {return 0;}

    let mut res = 0;
    
    let lead_segment = **&segments_left.chars().collect::<Vec<char>>().first().unwrap();
    if lead_segment == '.' && periods_left > 0 {
        res += get_matches(periods_left-1, values_left, &segments_left[1..segments_left.len()], false);
    }
    else if lead_segment == '#' && segments_left.len() > 0 {
        // temp = "#" * values[0]
        let mut temp = String::new();
        let value = values_left.split(',').collect::<Vec<&str>>().first().unwrap().parse::<i64>().unwrap() as usize;
        for _ in 0..value {temp.push('#');}
        
        if must_be_period == true {return 0;}
        // Check if OK
        else if segments_left.starts_with(&temp) {
            // OK
            let x = {if values_left.contains(',') {2} else {1}};
            res += get_matches(periods_left, &values_left[x..], &segments_left[value..], true);
        }
        else {
            // NOT OK
            return 0;
        }
    }
    else {
        // Always check for period
        res += get_matches(periods_left-1, values_left, &segments_left[1..], false);
        // If it can be something else, try
        if must_be_period == false && values_left.len() > 0 {
            // temp = "#" * values[0]
            let mut temp = String::new();
            let value = values_left.split(',').collect::<Vec<&str>>().first().unwrap().parse::<i64>().unwrap() as usize;
            for _ in 0..value {temp.push('#');}

            if check_match(&segments_left[0..value], &temp) {
                let x = {if values_left.contains(',') {2} else {1}};
                res += get_matches(periods_left, &values_left[x..], &segments_left[value..], true);
            }
        }
    }
 
    return res;
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

// fn apply_mask(values: &Vec<i64>, perm: &Vec<i64>) -> String {
//     let mut res: String = String::new();
//     for i in 0..values.len() {
//         for p in 0..perm[i] {
//             res.push('.');
//         }
//         for j in 0..values[i] {
//             res.push('#');
//         }
//     }
//     for p in 0..*perm.last().unwrap() {
//         res.push('.');
//     }
//     return res;
// }

fn create_perms(periods_left: i64, spaces_left: i64, min: i64) -> Vec<Vec<i64>> {
    if spaces_left == 1 {
        return vec![vec![periods_left]];
    }
    let mut i: i64 = periods_left;
    let mut res: Vec<Vec<i64>> = Vec::new();
    while i >= min {
        for mut v in create_perms(periods_left-i, spaces_left-1, 1) {
            let mut temp: Vec<i64> = vec![i];
            temp.append(&mut v);
            res.push(temp);
        }
        i -= 1;
    }
    return res;
}