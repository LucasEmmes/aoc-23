use std::cmp::Ordering;
use std::collections::HashMap;

#[derive(Eq, Hash, PartialEq)]
enum HandType {
    FiveOfAKind,
    FourOfAKind,
    FullHouse,
    ThreeOfAKind,
    TwoPair,
    OnePair,
    HighCard
}

fn main() {
    let mut evaluate: HashMap<char, i64> = HashMap::new();
    evaluate.insert('A', 13);
    evaluate.insert('K', 12);
    evaluate.insert('Q', 11);
    evaluate.insert('J', 10);
    evaluate.insert('T', 9);
    evaluate.insert('9', 8);
    evaluate.insert('8', 7);
    evaluate.insert('7', 6);
    evaluate.insert('6', 5);
    evaluate.insert('5', 4);
    evaluate.insert('4', 3);
    evaluate.insert('3', 2);
    evaluate.insert('2', 1);

    let mut hand_evaluate: HashMap<HandType, i8> = HashMap::new();
    hand_evaluate.insert(HandType::FiveOfAKind, 6);
    hand_evaluate.insert(HandType::FourOfAKind, 5);
    hand_evaluate.insert(HandType::FullHouse, 4);
    hand_evaluate.insert(HandType::ThreeOfAKind, 3);
    hand_evaluate.insert(HandType::TwoPair, 2);
    hand_evaluate.insert(HandType::OnePair, 1);
    hand_evaluate.insert(HandType::HighCard, 0);

    let input: String = std::fs::read_to_string("input.txt").expect("");
    let input_lines: Vec<&str> = input.split("\n").filter(|x| x.len() > 0).collect::<Vec<&str>>();

    let mut hands: Vec<(&str, i64)> = Vec::new();
    for line in input_lines {
        let cards = line.split(" ").collect::<Vec<&str>>()[0];
        let bid = line.split(" ").collect::<Vec<&str>>()[1].parse::<i64>().unwrap();
        let hand = (cards, bid);
        get_hand_type_p1(&hand, &evaluate);
        hands.push(hand);
    }

    hands.sort_by(|a, b| custom_comp(a, b, &evaluate, &hand_evaluate, &"p1")); // Sorts ascending

    let mut p1 = 0;
    for i in 0..hands.len() {
        p1 += hands[i].1 * (i as i64 +1);
    }
    println!("P1 {}", p1);
    
    evaluate.insert('J', 0);
    hands.sort_by(|a, b| custom_comp(a, b, &evaluate, &hand_evaluate, &"p2")); // Sorts ascending
    
    let mut p2 = 0;
    for i in 0..hands.len() {
        p2 += hands[i].1 * (i as i64 +1);
    }
    println!("P2 {}", p2);
    
}

fn get_hand_type_p1(hand: &(&str, i64), evaluate: &HashMap<char, i64>) -> HandType {
    let mut values: [i8; 14] = [0; 14];
    for c in hand.0.chars() {
        values[*evaluate.get(&c).unwrap() as usize] += 1;
    }
    values.sort();

    return match values {
        [0,0,0,0,0,0,0,0,0,0,0,0,0,5] => HandType::FiveOfAKind,
        [0,0,0,0,0,0,0,0,0,0,0,0,1,4] => HandType::FourOfAKind,
        [0,0,0,0,0,0,0,0,0,0,0,0,2,3] => HandType::FullHouse,
        [0,0,0,0,0,0,0,0,0,0,0,1,1,3] => HandType::ThreeOfAKind,
        [0,0,0,0,0,0,0,0,0,0,0,1,2,2] => HandType::TwoPair,
        [0,0,0,0,0,0,0,0,0,0,1,1,1,2] => HandType::OnePair,
        [0,0,0,0,0,0,0,0,0,1,1,1,1,1] => HandType::HighCard,
        _ => HandType::HighCard
    }
}

fn get_hand_type_p2(hand: &(&str, i64), evaluate: &HashMap<char, i64>) -> HandType {
    let mut values: [i8; 14] = [0; 14];
    let mut jokers: i8 = 0;
    for c in hand.0.chars() {
        if c == 'J' {jokers+=1;}
        else {
            values[*evaluate.get(&c).unwrap() as usize] += 1;
        }
    }
    values.sort();
    values[13] += jokers;

    return match values {
        [0,0,0,0,0,0,0,0,0,0,0,0,0,5] => HandType::FiveOfAKind,
        [0,0,0,0,0,0,0,0,0,0,0,0,1,4] => HandType::FourOfAKind,
        [0,0,0,0,0,0,0,0,0,0,0,0,2,3] => HandType::FullHouse,
        [0,0,0,0,0,0,0,0,0,0,0,1,1,3] => HandType::ThreeOfAKind,
        [0,0,0,0,0,0,0,0,0,0,0,1,2,2] => HandType::TwoPair,
        [0,0,0,0,0,0,0,0,0,0,1,1,1,2] => HandType::OnePair,
        [0,0,0,0,0,0,0,0,0,1,1,1,1,1] => HandType::HighCard,
        _ => HandType::HighCard
    }
}

fn custom_comp(a: &(&str, i64), b: &(&str, i64), evaluate: &HashMap<char, i64>, hand_evaluate: &HashMap<HandType, i8>, ctype: &str) -> Ordering {

    if ctype == "p1" {
        if hand_evaluate.get(&get_hand_type_p1(a, evaluate)) > hand_evaluate.get(&get_hand_type_p1(b, evaluate)) {
            return Ordering::Greater;
        }
        else if hand_evaluate.get(&get_hand_type_p1(a, evaluate)) < hand_evaluate.get(&get_hand_type_p1(b, evaluate)) {
            return Ordering::Less;
        }
    }
    else if ctype == "p2" {
        if hand_evaluate.get(&get_hand_type_p2(a, evaluate)) > hand_evaluate.get(&get_hand_type_p2(b, evaluate)) {
            return Ordering::Greater;
        }
        else if hand_evaluate.get(&get_hand_type_p2(a, evaluate)) < hand_evaluate.get(&get_hand_type_p2(b, evaluate)) {
            return Ordering::Less;
        }
    }
    

    for i in 0..5 {
        if evaluate.get(&a.0.chars().collect::<Vec<char>>()[i as usize]) > evaluate.get(&b.0.chars().collect::<Vec<char>>()[i as usize]) {
            return Ordering::Greater;
        }
        else if evaluate.get(&a.0.chars().collect::<Vec<char>>()[i as usize]) < evaluate.get(&b.0.chars().collect::<Vec<char>>()[i as usize]) {
            return Ordering::Less;
        }
    }
    
    return Ordering::Equal;
}