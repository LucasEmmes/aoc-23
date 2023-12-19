use core::fmt;
use std::{collections::HashMap, thread::current};

#[derive(Debug, Clone, PartialEq)]
enum Direction {
    Horizontal,
    Vertical,
    Wildcard
}

#[derive(Debug, Clone, Copy, Hash)]
struct Pos {
    y: i64,
    x: i64
}

impl fmt::Display for Pos {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        return write!(f, "({},{})", self.y, self.x);
    }
}

impl PartialEq for Pos {
    fn eq(&self, other: &Self) -> bool {
        return self.y == other.y && self.x == other.x;
    }
}

impl Eq for Pos {}

#[derive(Debug, Clone)]
struct Edge {
    pos: Pos,
    cost: i64
}

#[derive(Debug, Clone)]
struct Node {
    pos: Pos,
    parent: (Direction, Pos),
    lowest_cost: i64,
    edges: Vec<Edge>
}

impl PartialEq for Node {
    fn eq(&self, other: &Self) -> bool {
        return self.lowest_cost == other.lowest_cost;
    }
}
impl Eq for Node {}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        return self.lowest_cost.cmp(&other.lowest_cost);
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        return Some(self.cmp(other))
    }
}

fn get_direction(current: &Pos, next: &Pos) -> Direction {
    if current.y != next.y && current.x != next.x {
        return Direction::Wildcard;
    } else if current.y != next.y {
        return Direction::Vertical;
    } else if current.x != next.x {
        return Direction::Horizontal;
    }
    return Direction::Wildcard;
}

fn main() {
    let input: String = std::fs::read_to_string("demo.txt").expect("");
    let tiles: Vec<Vec<i64>> = input.split('\n').filter(|x| !x.is_empty()).map(|x| x.chars().map(|y| y.to_string().parse::<i64>().unwrap()).collect()).collect();

    let mut nodes: HashMap<Pos, Node> = HashMap::new();
    let mut directed_nodes: HashMap<(Pos, Direction), Node> = HashMap::new();
    let none_parent = Pos{y: -1, x: -1};

    for y in 0..tiles.len() {
        for x in 0..tiles[0].len() {
            let pos = Pos{y: y as i64, x: x as i64};
            let node = Node{pos:pos.clone(), parent:(Direction::Wildcard, none_parent.clone()), lowest_cost:i64::MAX, edges:Vec::new()};
            nodes.insert(pos, node);
        }
    }

    for y in 0..tiles.len() {
        for x in 0..tiles[0].len() {
            let pos = Pos{y: y as i64, x: x as i64};
            let mut current_node = nodes.get(&pos).unwrap().clone();
            
            let mut sums: [i64;4] = [0;4];

            for i in 0..3 {
                if pos.x > i as i64 {
                    let temp_cost = sums[0] + tiles[y][x-1-i];
                    sums[0] = temp_cost;
                    let temp_pos = Pos{y: y as i64, x: (x-1-i) as i64};
                    current_node.edges.push(Edge{pos: temp_pos, cost: temp_cost});
                }
                if pos.x < (tiles[0].len() - 1 - i) as i64 {
                    let temp_cost = sums[1] + tiles[y][x+1+i];
                    sums[1] = temp_cost;
                    let temp_pos = Pos{y: y as i64, x: (x+1+i) as i64};
                    current_node.edges.push(Edge{pos: temp_pos, cost: temp_cost});
                }
                
                if pos.y > i as i64 {
                    let temp_cost = sums[2] + tiles[y-1-i][x];
                    sums[2] = temp_cost;
                    let temp_pos = Pos{y: (y-1-i) as i64 as i64, x: x as i64};
                    current_node.edges.push(Edge{pos: temp_pos, cost: temp_cost});
                }
                if pos.y < (tiles.len() - 1 - i) as i64 {
                    let temp_cost = sums[3] + tiles[y+1+i][x];
                    sums[3] = temp_cost;
                    let temp_pos = Pos{y: (y+1+i) as i64, x: x as i64};
                    current_node.edges.push(Edge{pos: temp_pos, cost: temp_cost});
                }
            }
            nodes.insert(pos, current_node);
        }
    }

    nodes.insert(none_parent.clone(), Node{pos: none_parent.clone(), parent:(Direction::Wildcard, none_parent.clone()), lowest_cost: 0, edges: Vec::new()});
    let startpos = Pos{y:0,x:0};
    let mut start = nodes.get(&startpos).unwrap().clone();
    start.lowest_cost = 0;
    nodes.insert(start.pos.clone(), start.clone());
    let endpos = Pos{y: tiles.len() as i64-1, x: tiles[0].len() as i64 - 1};
    let mut queue: Vec<Node> = vec![start];

    let mut progress = String::new();
    while queue.len() > 0 && queue.last().unwrap().pos != endpos {
        let current_node = queue.pop().unwrap();
        for Edge{pos: temp_pos, cost} in current_node.edges {
            let mut next_node = nodes.get(&temp_pos).unwrap().clone();
            let next_direction = get_direction(&current_node.pos, &next_node.pos);
            let allowed: bool = {
                if current_node.parent.0 == Direction::Wildcard {true}
                else {
                    current_node.parent.0 != next_direction
                }
            };

            if allowed && (current_node.lowest_cost + cost) < next_node.lowest_cost {
                next_node.lowest_cost = current_node.lowest_cost + cost;
                next_node.parent = (next_direction, current_node.pos.clone());
                queue.push(next_node.clone());
                progress.push_str(&next_node.clone().pos.to_string());
                nodes.insert(temp_pos, next_node);
            }
        }
        queue.sort();
        queue.reverse();
    }


    println!("P1 {}", nodes.get(&endpos).unwrap().clone().lowest_cost);

}
