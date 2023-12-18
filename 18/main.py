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
    """
    Check if point is inside polygon defined by edges
    Does so by looking to the right and counting number of edges crossed.
    Even = outside, Odd = inside
    """
    cnt = 0
    for edge in edges:
        is_left_of_edge = point.x < max(edge.a.x, edge.b.x)
        is_between_points_vertical = (point.y < edge.a.y and point.y > edge.b.y) \
            or (point.y < edge.b.y and point.y > edge.a.y)
        
        if is_left_of_edge and is_between_points_vertical:
            cnt += 1
    return cnt % 2 == 1



def find_expanded_coord(corner: Pos, edges: List[Edge]) -> Pos:
    """
    Determines which direction a corner should expand to make up for grid-alignment
    It does this by looking at the 4 positions offset by 0.5 relative top-left, top-right, bottom-left, bottom-right to the corner,
    and checking whether they are inside or outside the polygon.
    
    1 position will be an outlier. If this outlier is outside, we move the corner there.
    If the outlier is inside, we move the corner to the position opposite the outlier.
    This way we will "expand" the polygon by 0.5 in every dimension.

    E.g. looking at the starting corner of the demo code, it would move from (0,0) to (-0.5, -0.5)
    """
    a = Pos(corner.y+0.5, corner.x+0.5)
    b = Pos(corner.y-0.5, corner.x+0.5)
    c = Pos(corner.y-0.5, corner.x-0.5)
    d = Pos(corner.y+0.5, corner.x-0.5)
    A = is_inside(a, edges)
    B = is_inside(b, edges)
    C = is_inside(c, edges)
    D = is_inside(d, edges)
    if not A and (B and C and D): return a
    if not B and (A and C and D): return b
    if not C and (B and A and D): return c
    if not D and (B and C and a): return d
    if A and not (B or C or D): return c
    if B and not (A or C or D): return d
    if C and not (B or A or D): return a
    if D and not (B or C or A): return b



def calc_volume(coords: List[Pos]) -> float:
    """
    Shoelace formula for calculating area of polygon
    """
    left = 0
    right = 0
    for i in range(0,len(coords)-1):
        left += coords[i].x*coords[i+1].y
        right += coords[i+1].x*coords[i].y
    return abs(left - right) * 0.5



def solve(data: List[Tuple[int, int]]) -> float:
    """
    Solve the task by calculating the volume
    """
    coords: List[Pos] = [Pos(0,0)]
    edges: List[Edge] = []
    coords_expanded: List[Pos] = []

    for (direction, amount) in data:
        current_pos = copy(coords[-1])

        if direction == "R": current_pos.x += amount
        if direction == "L": current_pos.x -= amount
        if direction == "U": current_pos.y -= amount
        if direction == "D": current_pos.y += amount

        edges.append(Edge(copy(coords[-1]), copy(current_pos)))
        coords.append(copy(current_pos))
    edges.append(Edge(copy(coords[-1]), copy(coords[0])))

    for pos in coords:
        coords_expanded.append(find_expanded_coord(pos, edges))

    return calc_volume(coords_expanded)



def main(file):
    with open(file, "r") as f:
        lines = list(filter(lambda x: len(x) > 0, f.read().split("\n")))
    
    # P1 -----------------------------------------------------------------------
    data_p1: List[Tuple[int, int]] = []

    for line in lines:
        direction, amount, _ = line.split(" ")
        amount = int(amount)
        data_p1.append((direction, amount))

    print(f"P1 {solve(data_p1)}")

    # P2 -----------------------------------------------------------------------
    data_p2: List[Tuple[int, int]] = []
    
    for line in lines:
        _, _, color = line.split(" ")
        amount = int(color[2:7], 16)
        direction = int(color[7])
        direction = "RDLU"[direction]
        data_p2.append((direction, amount))

    print(f"P2 {solve(data_p2)}")



if __name__ == "__main__":
    file = "demo.txt"
    if len(sys.argv) == 2:
        file = sys.argv[1]
    main(file)