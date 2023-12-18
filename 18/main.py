from typing import Dict, List, Tuple
from dataclasses import dataclass
import sys
from copy import copy
import math

@dataclass
class Pos:
    y: int
    x: int

@dataclass
class Edge:
    a: Pos
    b: Pos

def is_inside(point: Pos, edges: List[Edge]) -> bool:
    cnt = 0
    for edge in edges:
        if point.x < edge.a.x != point.x < edge.b.x and \
            point.x < edge.a.x + ((point.y-edge.a.y)/(edge.b.y-edge.a.y))*(edge.b.x-edge.a.x):
            cnt += 1
    return cnt %2 == 1

def main(file):
    # Read into 2D array of ints
    with open(file, "r") as f:
        lines = f.read().split("\n")
    lines.pop()
    
    coords: List[Pos] = [Pos(0,0)]
    edges: List[Edge] = []

    p1 = 0

    current_coord = Pos(0,0)
    for line in lines:
        direction, amount, color = line.split(" ")
        amount = int(amount)
        if direction == "R":
            current_coord.x += amount
        if direction == "L":
            current_coord.x -= amount
        if direction == "U":
            current_coord.y -= amount
        if direction == "D":
            current_coord.y += amount
        p1 += amount
        coords.append(copy(current_coord))
        edges.append(Edge(copy(coords[-1]), copy(current_coord)))

    edges.append(Edge(copy(coords[-1]), copy(coords[0])))
    
    print(is_inside(Pos(1,1), edges))

    # left = 0
    # right = 0
    # for i in range(0,len(coords)-1):
    #     left += coords[i].x*coords[i+1].y
    #     right += coords[i+1].x*coords[i].y
    # p1 += abs(left - right) * 0.5
    # print(f"P1 {p1}")



if __name__ == "__main__":
    file = "demo.txt"
    if len(sys.argv) == 2:
        file = sys.argv[1]
    main(file)