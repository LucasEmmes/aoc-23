from typing import Dict, List, Tuple
from dataclasses import dataclass
import sys
from queue import PriorityQueue
from enum import Enum

class Direction(Enum):
    WILDCARD = 0
    HORIZONTAL = 1
    VERTICAL = 2

@dataclass
class Node:
    y: int
    x: int
    parent: 'Node'
    direction: Direction
    lowest_cost: int
    edges: List[Tuple[int, 'Node']]

    def __lt__(self, other: 'Node'):
        return self.lowest_cost < other.lowest_cost
    
    def __gt__(self, other: 'Node'):
        return self.lowest_cost > other.lowest_cost
    
    def __eq__(self, other: 'Node'):
        return self.lowest_cost == other.lowest_cost
    
    def __repr__(self) -> str:
        return f"Pos: ({self.y},{self.x}) Edges: {[f'({edge[0]}, ({edge[1].y},{edge[1].x}))' for edge in self.edges]}"

def main(file):
    # Read into 2D array of ints
    with open(file, "r") as f:
        values = [[int(c) for c in line] for line in f.read().split("\n")[:-1]]

    # Storage for nodes
    nodes_ver: Dict[(int, int), Node] = {}  # Nodes where parent comes from horizontal
    nodes_hor: Dict[(int, int), Node] = {}  # Nodes where parent comes from vertical

    # Initialize empty nodes
    for y in range(0, values.__len__()):
        for x in range(0, values[0].__len__()):
            nodes_ver[(y, x)] = Node(y, x, None, Direction.HORIZONTAL, float('inf'), [])
            nodes_hor[(y, x)] = Node(y, x, None, Direction.VERTICAL, float('inf'), [])

    # Make connections
    for y in range(0, values.__len__()):
        for x in range(0, values[0].__len__()):
            current_node_ver = nodes_ver[(y, x)]
            current_node_hor = nodes_hor[(y, x)]
            # Check 3 steps in each direction
            sums = [0, 0, 0, 0]
            for i in range(3, 10):
                if x > i:
                    temp_cost = sums[0] + values[y][x-1-i]
                    sums[0] = temp_cost
                    # current_node_ver.edges.append((temp_cost, nodes_hor[(y, x-1-i)]))
                    current_node_ver.edges.append((sum([ values[y][x-1-j] for j in range(i+1)]), nodes_hor[(y, x-1-i)]))

                if x < values[0].__len__()-1-i:
                    temp_cost = sums[1] + values[y][x+1+i]
                    sums[1] = temp_cost
                    # current_node_ver.edges.append((temp_cost, nodes_hor[(y, x+1+i)]))
                    current_node_ver.edges.append((sum([ values[y][x+1+j] for j in range(i+1)]), nodes_hor[(y, x+1+i)]))

                if y > i:
                    temp_cost = sums[2] + values[y-1-i][x]
                    sums[2] = temp_cost
                    # current_node_hor.edges.append((temp_cost, nodes_ver[(y-1-i, x)]))
                    current_node_hor.edges.append((sum([ values[y-1-j][x] for j in range(i+1)]), nodes_ver[(y-1-i, x)]))

                if y < values.__len__()-1-i:
                    temp_cost = sums[3] + values[y+1+i][x]
                    sums[3] = temp_cost
                    # current_node_hor.edges.append((temp_cost, nodes_ver[(y+1+i, x)]))
                    current_node_hor.edges.append((sum([ values[y+1+j][x] for j in range(i+1)]), nodes_ver[(y+1+i, x)]))

    # Dijkstra setup
    start_pos = (0,0)
    start_ver = nodes_ver[start_pos]
    start_hor = nodes_hor[start_pos]

    end_pos = (len(values)-1, len(values[0])-1)
    end_ver = nodes_ver[end_pos]
    end_hor = nodes_hor[end_pos]

    queue: PriorityQueue[Node] = PriorityQueue()
    start_ver.lowest_cost = 0
    queue.put(start_ver)
    start_hor.lowest_cost = 0
    queue.put(start_hor)
    current_node = None

    # while queue.qsize() > 0:
    while queue.qsize() > 0:
        current_node = queue.get()
        for cost, next_node in current_node.edges:
            if (current_node.lowest_cost + cost) < next_node.lowest_cost:
                next_node.lowest_cost = current_node.lowest_cost + cost
                next_node.parent = current_node
                queue.put(next_node)

    if end_ver.lowest_cost < end_hor.lowest_cost:
        current_node = end_ver
    else:
        current_node = end_hor

    print(f"P1 {current_node.lowest_cost}")

    # while current_node is not start_hor and current_node is not start_ver:
    #     if current_node.direction == Direction.HORIZONTAL:
    #         for y in range(current_node.y, current_node.parent.y, 1 if current_node.y < current_node.parent.y else -1):
    #             values[y][current_node.x] = "|"
    #     elif current_node.direction == Direction.VERTICAL:
    #         for x in range(current_node.x, current_node.parent.x, 1 if current_node.x < current_node.parent.x else -1):
    #             values[current_node.y][x] = "-"
    #     current_node = current_node.parent
                
    # for row in values:
    #     for v in row:
    #         print(str(v), end="")
    #     print()

if __name__ == "__main__":
    file = "demo.txt"
    if len(sys.argv) == 2:
        file = sys.argv[1]
    main(file)