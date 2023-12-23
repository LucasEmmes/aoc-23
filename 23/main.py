from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
import sys
from copy import copy, deepcopy
import math

@dataclass
class Pos:
    x: int
    y: int

@dataclass
class Tile:
    pos: Pos

@dataclass
class FloorTile(Tile):
    a: Pos
    b: Pos

@dataclass
class Slope(Tile):
    next_tile: Pos

@dataclass
class Node(Tile):
    lowes_known_cost: int
    edges: List[Tuple[int, Pos]]

def main(file):
    with open(file, "r") as f:
        lines = list(filter(lambda x: len(x) > 0, f.read().split("\n")))

    # https://www.geeksforgeeks.org/find-longest-path-directed-acyclic-graph/

    # regular floor tiles, slopes, and juntions (floor tiles that don't touch other floor tiles)
    # any regular floor tile will touch exactly two other floor tiles, or one floor tile and one slope tile

    # map out all regular floor tiles with their "left" and "right" paths
    # map out all slope tiles with their one neccessary directed path
    # map out all junctions. If you can go the direction of a slope, follow the chain until you get to another junction (or the end)

if __name__ == "__main__":
    file = "demo.txt"
    if len(sys.argv) == 2:
        file = sys.argv[1]
    main(file)