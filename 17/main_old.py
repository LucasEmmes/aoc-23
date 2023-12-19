from typing import Dict, List, Tuple, Set, Deque
import sys
from dataclasses import dataclass

@dataclass
class Node:
    y: int
    x: int
    parent: 'Node'
    lowest_cost: int
    edges: List[Tuple[int, int, int]]

    def __lt__(self, other: 'Node'):
        return self.lowest_cost < other.lowest_cost
    
    def __gt__(self, other: 'Node'):
        return self.lowest_cost > other.lowest_cost
    
    def __eq__(self, other: 'Node'):
        return self.lowest_cost == other.lowest_cost

def get_direction(current: Node, next: Node = None) -> int:
    if next is None:
        if current.parent is None: return -1
        if current.parent.y != current.y: return 1
        if current.parent.x != current.x: return 2
        else: return 0
    else:
        if current.y != next.y: return 1
        if current.x != next.x: return 2
        else: return 0



def main(file):
    with open(file, "r") as f:
        lines = [[c for c in line] for line in f.read().split("\n")[:-1]]
        values = [[int(c) for c in line] for line in lines]

    nodes: Dict[(int, int), Node] = {}
    nodeset: Set[(int, int)] = set()

    for y in range(0, lines.__len__()):
        for x in range(0, lines[0].__len__()):
            nodes[(y, x)] = Node(y, x, None, float('inf'), [])
            nodeset.add((y, x))

    for y in range(0, lines.__len__()):
        for x in range(0, lines[0].__len__()):
            current_node = nodes[(y, x)]

            for i in range(3):
                if x > i: current_node.edges.append((y, x-1-i, sum([ values[y][x-1-j] for j in range(i+1)])))
                if x < lines[0].__len__()-1-i: current_node.edges.append((y, x+1+i, sum([ values[y][x+1+j] for j in range(i+1)])))
                if y > i: current_node.edges.append((y-1-i, x, sum([ values[y-1-j][x] for j in range(i+1)])))
                if y < lines.__len__()-1-i: current_node.edges.append((y+1+i, x, sum([ values[y+1+j][x] for j in range(i+1)])))
            

    start = nodes[(0,0)]
    start.lowest_cost = 0
    end = nodes[(lines.__len__()-1, lines[0].__len__()-1)]
    queue: List[Node] = list(nodes.values())
    queue.sort()
    current_node = start
    # progress = ""

    while queue[0] != end:
        current_node = queue.pop(0)
        # print(f"Starting inspection of {current_node}")
        for (y, x, cost) in current_node.edges:
            next_node = nodes[(y, x)]
            # Check if the steps are forbidden
            is_forbidden = get_direction(current_node) == get_direction(current_node, next_node)
            # print("Looking at jump from Pos { y: " + str(current_node.y) + ", x: " + str(current_node.x) + " } to Pos { y: " + str(y) + ", x: " + str(x) + " }: ", end="")
            if not is_forbidden and current_node.lowest_cost + cost < next_node.lowest_cost:
                next_node.lowest_cost = current_node.lowest_cost + cost
                next_node.parent = current_node
                # queue.append(next_node)
                # progress += f"({next_node.y},{next_node.x})"
                # print("allowed!")
            # else:
            #     print("blocked!")

        queue.sort()
        print([node.lowest_cost for node in queue])


    # print(progress)
    print(end.lowest_cost)

if __name__ == "__main__":
    file = "demo.txt"
    if len(sys.argv) == 2:
        file = sys.argv[1]
    main(file)