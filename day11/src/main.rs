fn main() {

    let input: String = std::fs::read_to_string("input.txt").expect("");
    let input_lines: Vec<&str> = input.split('\n').filter(|x| !x.is_empty()).collect::<Vec<&str>>();

    let mut map: Vec<Vec<bool>> = Vec::new();

    // Make to rows
    for line in &input_lines {
        let row = line.chars().map(|x| x=='#').collect::<Vec<bool>>();
        map.push(row);
    }

    // Expand rows with no galaxies
    let mut galaxies_duplicated = 0;
    for (i, row) in map.clone().into_iter().enumerate() {
        if !row.into_iter().reduce(|a, b| a | b).unwrap() {
            map.insert(i+galaxies_duplicated, vec![false; map[0].len()]);
            galaxies_duplicated += 1;
        }
    }

    // Iterate over cols
    let mut i: usize = 0;
    while i < map[0].len() {
        let mut has_galaxies = false;
        for row in &map {
            has_galaxies |= row[i];
        }
        if !has_galaxies {
            for row in &mut map {
                row.insert(i, false);
            }
            i+=1
        }
        i+=1;
    }
    
    // SETUP DONE

    let mut galaxies: Vec<(i64, i64)> = Vec::new();
    for y in 0..map.len() {
        for x in 0..map[0].len() {
            if map[y][x] {
                galaxies.push((y as i64, x as i64));
            }
        }
    }

    let mut p1 = 0;
    for (i, galaxy) in galaxies.clone().into_iter().enumerate() {
        for other_galaxy in &galaxies[i+1..galaxies.len()] {
            p1 += (galaxy.0 - other_galaxy.0).abs() + (galaxy.1 - other_galaxy.1).abs();
        }
    }
    println!("P1 {p1}");

    map.clear();
    // Make to rows
    for line in &input_lines {
        let row = line.chars().map(|x| x=='#').collect::<Vec<bool>>();
        map.push(row);
    }

    galaxies.clear();
    for y in 0..map.len() {
        for x in 0..map[0].len() {
            if map[y][x] {
                galaxies.push((y as i64, x as i64));
            }
        }
    }

    let mut p2 = 0;
    for (i, galaxy) in galaxies.clone().into_iter().enumerate() {
        for other_galaxy in &galaxies[i+1..galaxies.len()] {
            let y_max = i64::max(galaxy.0, other_galaxy.0) as usize;
            let y_min = i64::min(galaxy.0, other_galaxy.0) as usize;
            let x_max = i64::max(galaxy.1, other_galaxy.1) as usize;
            let x_min = i64::min(galaxy.1, other_galaxy.1) as usize;
            
            let empty_rows = count_empty_rows(&map, y_min, y_max);
            let empty_cols = count_empty_cols(&map, x_min, x_max);
            p2 += (galaxy.0 - other_galaxy.0).abs() + (galaxy.1 - other_galaxy.1).abs() + empty_cols*999999 + empty_rows*999999;
        }
    }
    println!("P2 {p2}");


}

fn row_empty(map: &Vec<Vec<bool>>, row: usize) -> bool {
    !map[row].clone().into_iter().reduce(|a, b| a | b).unwrap()
}

fn col_empty(map: &Vec<Vec<bool>>, col: usize) -> bool {
    for row in map {
        if row[col] {return false;}
    }
    true
}

fn count_empty_rows(map: &Vec<Vec<bool>>, start: usize, stop: usize) -> i64 {
    let mut res = 0;
    for i in start+1..stop {
        if row_empty(map, i) {res += 1;}
    }
    res
}

fn count_empty_cols(map: &Vec<Vec<bool>>, start: usize, stop: usize) -> i64 {
    let mut res = 0;
    for i in start+1..stop {
        if col_empty(map, i) {res += 1;}
    }
    res
}