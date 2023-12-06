fn main() {

    let input: String = std::fs::read_to_string("input.txt").expect("");
    let input_lines: Vec<&str> = input.split("\n").collect::<Vec<&str>>();

    let times = input_lines[0].split(" ").filter(|x| x.len() > 0 && x != &"Time:").map(|x| x.parse::<f64>().unwrap()).collect::<Vec<f64>>();
    let distances = input_lines[1].split(" ").filter(|x| x.len() > 0 && x != &"Distance:").map(|x| x.parse::<f64>().unwrap()).collect::<Vec<f64>>();

    let mut p1 = 1;
    for i in 0..times.len() {
        p1 *= get_possibilities(times[i], distances[i]);
    }
    println!("P1 {}", p1);

    let time = input_lines[0].split(" ").filter(|x| x.len() > 0 && x != &"Time:").collect::<Vec<&str>>().join("").parse::<f64>().unwrap();
    let distance = input_lines[1].split(" ").filter(|x| x.len() > 0 && x != &"Distance:").collect::<Vec<&str>>().join("").parse::<f64>().unwrap();

    println!("P2 {}", get_possibilities(time, distance));

}

fn get_possibilities(time: f64, distance: f64) -> i64 {
    let x1 = ((-1.0*time + f64::sqrt(time*time - 4.0*distance))/-2.0 + 1.0).floor() as i64;
    let x2 = ((-1.0*time - f64::sqrt(time*time - 4.0*distance))/-2.0 - 1.0).ceil() as i64;
    return x2-x1+1;
}