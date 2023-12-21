from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
import sys
from copy import copy, deepcopy
import math

@dataclass
class Node:
    pos: Tuple[int, int]
    up: 'Node' = None
    down: 'Node' = None
    left: 'Node' = None
    right: 'Node' = None

def main(file):
    with open(file, "r") as f:
        lines = list(filter(lambda x: len(x) > 0, f.read().split("\n")))

    nodes: Dict[Tuple[int, int], Node] = {}

    start = (0,0)
    garden = []
    for y, line in enumerate(lines):
        temp = []
        for x, i in enumerate(line):
            if i != "#": nodes[(y, x)] = Node(pos=(y,x))
            if i == "S":
                start = (y, x)

    for y in range(0, len(lines)):
        for x in range(0, len(lines[0])):
            if y > 0:
                if lines[y][x] != "#" and lines[y-1][x] != "#":
                    nodes[(y, x)].up = nodes[(y-1, x)]
            if y < len(lines)-1:
                if lines[y][x] != "#" and lines[y+1][x] != "#":
                    nodes[(y, x)].down = nodes[(y+1, x)]
            if x > 0:
                if lines[y][x] != "#" and lines[y][x-1] != "#":
                    nodes[(y, x)].left = nodes[(y, x-1)]
            if x < len(lines[0])-1:
                if lines[y][x] != "#" and lines[y][x+1] != "#":
                    nodes[(y, x)].right = nodes[(y, x+1)]
    
    
    
                    
    # seen: Set[Node] = set()
    current_step: Set[Node] = set([start])
    next_step: Set[Node] = set()
    

    for i in range(64):
        while len(current_step) > 0:
            pos = current_step.pop()
            node = nodes[pos]
            # seen.add(pos)
            
            if node.up is not None and node.up.pos not in current_step:
                next_step.add(node.up.pos)
            if node.down is not None and node.down.pos not in current_step:
                next_step.add(node.down.pos)
            if node.left is not None and node.left.pos not in current_step:
                next_step.add(node.left.pos)
            if node.right is not None and node.right.pos not in current_step:
                next_step.add(node.right.pos)

        current_step = next_step
        next_step = set()
            
    print(len(current_step))


if __name__ == "__main__":
    file = "demo.txt"
    if len(sys.argv) == 2:
        file = sys.argv[1]
    main(file)