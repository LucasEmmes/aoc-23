use std::collections::HashMap;

fn main() {
    // let now = std::time::Instant::now();
    let input: String = std::fs::read_to_string("input.txt").expect("");
    let mut map: Vec<Vec<char>> = input.split('\n').filter(|x| !x.is_empty()).map(|x| x.chars().collect()).collect();

    tilt_north(&mut map);
    println!("P1 {}", calc_load(&map));

    let mut memo: HashMap<(String, i64), (Vec<Vec<char>>, i64)> = HashMap::new();
    
    let mut i: i64 = 1;
    while i < 4000000000 {
        let s = stringify(&map);
        let key = (s, i%4);
        if memo.contains_key(&key) {
            let (v, n) = memo.get(&key).unwrap();
            map = v.clone();
            let d = i - n;
            let D = (4000000000 - i) / d;
            i += d*D;
        } else {
            if i%4 == 0 {
                tilt_north(&mut map);
            }
            else if i%4 == 1 {
                tilt_west(&mut map);
            }
            else if i%4 == 2 {
                tilt_south(&mut map);
            }
            else if i%4 == 3 {
                tilt_east(&mut map);
            }

            memo.insert(key, (map.clone(), i));
        }
        
        i += 1;
    }

    println!("P2 {}", calc_load(&map));

}

fn calc_load(map: &Vec<Vec<char>>) -> i64 {
    let mut load = 0;
    for x in 0..map[0].len() {
        for y in 0..map.len() {
            if map[y][x] == 'O' {
                load += (map.len()-y) as i64;
            }
        }
    }
    return load;
}

fn stringify(map: &Vec<Vec<char>>) -> String {
    return map.clone().into_iter().map(|x| x.iter().collect::<String>()).reduce(|a, b| a + &b).unwrap();
}

fn tilt_north(map: &mut Vec<Vec<char>>) {
    for x in 0..map[0].len() {
        for _ in 1..map.len() {
            for y in 1..map.len() {
                if map[y][x] == 'O' && map[y-1][x] == '.' {
                    map[y][x] = '.';
                    map[y-1][x] = 'O';
                }
            }
        }
    }
}

fn tilt_south(map: &mut Vec<Vec<char>>) {
    for x in 0..map[0].len() {
        for _ in (0..map.len()-1).rev() {
            for y in (0..map.len()-1).rev() {
                if map[y][x] == 'O' && map[y+1][x] == '.' {
                    map[y][x] = '.';
                    map[y+1][x] = 'O';
                }
            }
        }
    }
}

fn tilt_west(map: &mut Vec<Vec<char>>) {
    for y in 0..map.len() {
        for _ in 1..map[0].len() {
            for x in 1..map[0].len() {
                if map[y][x] == 'O' && map[y][x-1] == '.' {
                    map[y][x] = '.';
                    map[y][x-1] = 'O';
                }
            }
        }
    }
}

fn tilt_east(map: &mut Vec<Vec<char>>) {
    for y in 0..map.len() {
        for _ in (0..map[0].len()-1).rev() {
            for x in (0..map[0].len()-1).rev() {
                if map[y][x] == 'O' && map[y][x+1] == '.' {
                    map[y][x] = '.';
                    map[y][x+1] = 'O';
                }
            }
        }
    }
}