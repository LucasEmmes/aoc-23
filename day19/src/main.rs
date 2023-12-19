use std::ops::RangeInclusive;
use std::collections::HashMap;

#[derive(Debug, Clone)]
struct MultiRange {
    ranges: Vec<RangeInclusive<i64>>
}

impl MultiRange {
    fn make(start: i64, stop: i64) -> Self {
        MultiRange{ranges: vec![start..=stop]}
    }
    
    fn from_range(range: RangeInclusive<i64>) -> Self {
        MultiRange{ranges: vec![range]}
    }

    fn new() -> Self {
        MultiRange{ranges:Vec::new()}
    }

    fn len(&self) -> usize {
        let mut len: usize = 0;
        for range in &self.ranges {
            len += (range.end() - range.start()) as usize;
        }
        len
    }

    fn contains(&self, n: i64) -> bool {
        for range in &self.ranges {
            if range.contains(&n) {return true;}
        }
        false
    }

    fn compress(&mut self) {
        self.ranges.sort_by_key(|x| *x.start());
        self.ranges.reverse();
        let mut temp = MultiRange::from_range(self.ranges.pop().unwrap());
        while !self.ranges.is_empty() {
            temp = get_range_union(&temp, &MultiRange::from_range(self.ranges.pop().unwrap()));
        }
        self.ranges = temp.ranges;
    }
}

fn main() {
    
    let input: String = std::fs::read_to_string("input.txt").expect("");
    let sections = input.split("\n\n").collect::<Vec<&str>>();
    // let lines = input.split('\n').collect::<Vec<&str>>();
    let mut lines = sections[0].split('\n').collect::<Vec<&str>>();

    let mut known_rules: HashMap<&str, [MultiRange;4]> = HashMap::new();
    known_rules.insert("R", [MultiRange::make(0,0), MultiRange::make(0,0), MultiRange::make(0,0), MultiRange::make(0,0)]);
    known_rules.insert("A", [MultiRange::make(0,4000), MultiRange::make(0,4000), MultiRange::make(0,4000), MultiRange::make(0,4000)]);


    // println!("{:?}", get_definition(&vec!["m>1548:A"], "A"));

    // let mut i: usize = 0;
    // while lines.len() > 0 {
    //     if lines[i].is_empty() {break;}
    //     // Chop everything up
    //     let line = lines[i];
    //     let temp: Vec<&str> = line.split('{').collect::<Vec<&str>>();
    //     let rule_name = temp[0];
        
    //     // "s>2770:qs,m<1801:hdj,R"
    //     let raw_rule_string = &temp[1][..temp[1].len()-1];

    //     // ["s>2770:qs", "m<1801:hdj", "R"]
    //     let mut raw_rules = raw_rule_string.split(',').collect::<Vec<&str>>();
    //     let fallback = raw_rules.pop().unwrap();
        
    //     if rule_is_fully_defined(raw_rule_string, &known_rules) {
    //         known_rules.insert(rule_name, [MultiRange::make(0,0), MultiRange::make(0,0), MultiRange::make(0,0), MultiRange::make(0,0)]);
    //         lines.remove(i);
    //         if lines.len() == 0 {break;}
    //         i = i%lines.len();
    //     } else {
    //         i = (i+1)%lines.len();
    //     }
    // }
}

fn rule_is_fully_defined(raw_rule: &str, known_rules: &HashMap<&str,[MultiRange;4]>) -> bool {
    // INPUT: s>2770:qs,m<1801:hdj,R
    let mut rule_strings = raw_rule.split(',').collect::<Vec<&str>>();
    let fallback = rule_strings.pop().unwrap();
    if !known_rules.contains_key(fallback) {return false;}
    
    for rule in rule_strings {
        let temp = rule.split(':').collect::<Vec<&str>>();
        let destination = temp[1];
        
        if !known_rules.contains_key(destination) {return false;}
    }
    
    true
}

fn get_definition(raw_rules: &Vec<&str>, fallback: &str, known_rules: &HashMap<&str,[MultiRange;4]>) -> [MultiRange;4] {
    let mut ranges: Vec<[MultiRange;4]> = Vec::new();
    for raw_rule in raw_rules {
        let temp = raw_rule.split(":").collect::<Vec<&str>>();
        let rule_string = temp[0];
        let value = temp[1];
        
        let known = known_rules.get(value).unwrap();
        let current = get_range_map(rule_string);
        let mut tempranges: [MultiRange;4] = [MultiRange::make(0,4000), MultiRange::make(0,4000), MultiRange::make(0,4000), MultiRange::make(0,4000)];
        for i in 0..4 {
            tempranges[i] = get_range_overlap(&known[i], &current[i]);
        }
        ranges.push(tempranges);
    }
    
    // let mut result = known_rules.get(fallback).unwrap().clone();
    // for range in ranges {
    //     let mut tempranges: [MultiRange;4] = [MultiRange::make(0,4000), MultiRange::make(0,4000), MultiRange::make(0,4000), MultiRange::make(0,4000)];
    //     for i in 0..4 {
    //         tempranges[i] = get_range_overlap(&known[i], &current[i]);
    //     }
    // }

    [MultiRange::make(0,4000), MultiRange::make(0,4000), MultiRange::make(0,4000), MultiRange::make(0,4000)]
}

fn get_range_map(inp: &str) -> [MultiRange;4] {
    let attr: &str = &inp[..1];
    let cmp: &str = &inp[1..2];
    let n: i64 = inp[2..].parse::<i64>().unwrap();

    let mut ranges: [MultiRange;4] = [MultiRange::make(0,4000), MultiRange::make(0,4000), MultiRange::make(0,4000), MultiRange::make(0,4000)];
    let i: usize = {
        match attr {
            "x" => 0,
            "m" => 1,
            "a" => 2,
            "s" => 3,
            _ => 5,
        }
    };
    
    if cmp == "<" {
        ranges[i] = MultiRange::make(0,n-1);
    }
    else {
        ranges[i] = MultiRange::make(n+1,4000);
    }

    ranges
}

fn get_range_overlap(a: &MultiRange, b: &MultiRange) -> MultiRange {
    let mut overlap = MultiRange::new();
    for arange in &a.ranges {
        for brange in &b.ranges {
            let start = i64::max(*arange.start(), *brange.start());
            let end = i64::min(*arange.end(), *brange.end());
            if start < end {
                overlap.ranges.push(start..=end);
            }
        }
    }

    overlap
}

fn get_range_union(a: &MultiRange, b: &MultiRange) -> MultiRange {
    let mut union = MultiRange::new();
    for arange in &a.ranges {
        for brange in &b.ranges {
            if arange.end() < brange.start() || brange.end() < arange.start() {
                union.ranges.push(*arange.start()..=*arange.end());
                union.ranges.push(*brange.start()..=*brange.end());
            }
            else {
                let start = i64::min(*arange.start(), *brange.start());
                let end = i64::max(*arange.end(), *brange.end());
                union.ranges.push(start..=end);
            }
        }
    }

    union
}