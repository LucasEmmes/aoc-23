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

def area(n: int) -> int:
    return n**2 + 2*n + 1

def get_full(lines: List[str]) -> Tuple[int, int]:
    odd = even = 0

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == "#":
                if (x+y) % 2 == 0: even += 1
                else: odd += 1

    return (even, odd)

def get_t1(lines: List[str], direction: int) -> Tuple[int, int]:
    odd = even = 0
    HEIGHT = WIDTH = len(lines)
    HALF = HEIGHT // 2

    if direction == 0:
        # for y in range(0,HEIGHT):
        #     for x in range(0,WIDTH):
        #         if y in range(0, HALF) and x in range(0, HALF-y):
        #             print("#", end="")
        #         else:
        #             print(".", end="")
        #     print()
        for y in range(0, HALF):
            for x in range(0, HALF-y):
                if lines[y][x] == "#":
                    if (x+y) % 2 == 0: even += 1
                    else: odd += 1
    elif direction == 1:
        # for y in range(0,HEIGHT):
        #     for x in range(0,WIDTH):
        #         if y in range(0, HALF) and x in range(HALF+1+y, WIDTH):
        #             print("#", end="")
        #         else:
        #             print(".", end="")
        #     print()
        for y in range(0, HALF):
            for x in range(HALF+1+y, WIDTH):
                if lines[y][x] == "#":
                    if (x+y) % 2 == 0: even += 1
                    else: odd += 1
    elif direction == 2:
        # for y in range(0,HEIGHT):
        #     for x in range(0,WIDTH):
        #         if y in range(HALF+1, HEIGHT) and x in range(HALF+(WIDTH-y), WIDTH):
        #             print("#", end="")
        #         else:
        #             print(".", end="")
        #     print()
        for y in range(HALF+1, HEIGHT):
            for x in range(HALF+(WIDTH-y), WIDTH):
                if lines[y][x] == "#":
                    if (x+y) % 2 == 0: even += 1
                    else: odd += 1
    elif direction == 3:
        # for y in range(0,HEIGHT):
        #     for x in range(0,WIDTH):
        #         if y in range(HALF+1, HEIGHT) and x in range(0, max(0, y-HALF)):
        #             print("#", end="")
        #         else:
        #             print(".", end="")
        #     print()
        for y in range(HALF+1, HEIGHT):
            for x in range(0, max(0, y-HALF)):
                if lines[y][x] == "#":
                    if (x+y) % 2 == 0: even += 1
                    else: odd += 1

    return (even, odd)

def get_t2(lines: List[str], direction: int) -> Tuple[int, int]:
    odd = even = 0
    HEIGHT = WIDTH = len(lines)
    HALF = HEIGHT // 2

    if direction == 0:
        # for y in range(0,HEIGHT):
        #     for x in range(0,WIDTH):
        #         if y in range(0, HEIGHT) and x in range(max(0, HALF-y), WIDTH):
        #             print("#", end="")
        #         else:
        #             print(".", end="")
        #     print()
        for y in range(0, HEIGHT):
            for x in range(max(0, HALF-y), WIDTH):
                if lines[y][x] == "#":
                    if (x+y) % 2 == 0: even += 1
                    else: odd += 1
    elif direction == 1:
        # for y in range(0,HEIGHT):
        #     for x in range(0,WIDTH):
        #         if y in range(0, HEIGHT) and x in range(0, min(HALF+1+y, WIDTH)):
        #             print("#", end="")
        #         else:
        #             print(".", end="")
        #     print()
        for y in range(0, HEIGHT):
            for x in range(0, min(HALF+1+y, WIDTH)):
                if lines[y][x] == "#":
                    if (x+y) % 2 == 0: even += 1
                    else: odd += 1
    elif direction == 2:
        # for y in range(0,HEIGHT):
        #     for x in range(0,WIDTH):
        #         if y in range(0, HEIGHT) and x in range(0, min(WIDTH, HALF+WIDTH-y)):
        #             print("#", end="")
        #         else:
        #             print(".", end="")
        #     print()
        for y in range(0, HEIGHT):
            for x in range(0, min(WIDTH, HALF+WIDTH-y)):
                if lines[y][x] == "#":
                    if (x+y) % 2 == 0: even += 1
                    else: odd += 1
    elif direction == 3:
        # for y in range(0,HEIGHT):
        #     for x in range(0,WIDTH):
        #         if y in range(0, HEIGHT) and x in range(max(0, HALF-WIDTH+y+1), WIDTH):
        #             print("#", end="")
        #         else:
        #             print(".", end="")
        #     print()
        for y in range(0, HEIGHT):
            for x in range(max(0, HALF-WIDTH+y+1), WIDTH):
                if lines[y][x] == "#":
                    if (x+y) % 2 == 0: even += 1
                    else: odd += 1
    
    return (even, odd)

def get_t3(lines: List[str], direction: int) -> Tuple[int, int]:
    t2_even, t2_odd = get_t2(lines, direction)
    t1_even, t1_odd = get_t1(lines, (direction+1)%4)
    return (t2_even - t1_even, t2_odd - t1_odd) 

def main(file):
    with open(file, "r") as f:
        lines = list(filter(lambda x: len(x) > 0, f.read().split("\n")))
    
    even, odd = get_full(lines)

    if False:
        # print(even == get_t1(lines, 0)[0] + get_t2(lines, 0)[0])
        # print(odd == get_t1(lines, 0)[1] + get_t2(lines, 0)[1])

        # print(even == get_t1(lines, 1)[0] + get_t2(lines, 1)[0])
        # print(odd == get_t1(lines, 1)[1] + get_t2(lines, 1)[1])

        # print(even == get_t1(lines, 2)[0] + get_t2(lines, 2)[0])
        # print(odd == get_t1(lines, 2)[1] + get_t2(lines, 2)[1])

        # print(even == get_t1(lines, 3)[0] + get_t2(lines, 3)[0])
        # print(odd == get_t1(lines, 3)[1] + get_t2(lines, 3)[1])

        # print(even == get_t3(lines, 0)[0] + get_t1(lines, 0)[0] + get_t1(lines, 1)[0])
        # print(odd == get_t3(lines, 0)[1] + get_t1(lines, 0)[1] + get_t1(lines, 1)[1])

        # print(even == get_t3(lines, 1)[0] + get_t1(lines, 2)[0] + get_t1(lines, 1)[0])
        # print(odd == get_t3(lines, 1)[1] + get_t1(lines, 2)[1] + get_t1(lines, 1)[1])

        # print(even == get_t3(lines, 2)[0] + get_t1(lines, 2)[0] + get_t1(lines, 3)[0])
        # print(odd == get_t3(lines, 2)[1] + get_t1(lines, 2)[1] + get_t1(lines, 3)[1])

        # print(even == get_t3(lines, 3)[0] + get_t1(lines, 0)[0] + get_t1(lines, 3)[0])
        # print(odd == get_t3(lines, 3)[1] + get_t1(lines, 0)[1] + get_t1(lines, 3)[1])
        pass

    # Number of rocks at the edge of the radius
    t3 = [get_t3(lines, i) for i in range(4)]
    t3_even = sum([i[0] for i in t3])
    t3_odd = sum([i[1] for i in t3])

    t2 = [get_t2(lines, i) for i in range(4)]
    t2_even = sum([i[0] for i in t2])
    t2_odd = sum([i[1] for i in t2])

    t1 = [get_t1(lines, i) for i in range(4)]
    t1_even = sum([i[0] for i in t1])
    t1_odd = sum([i[1] for i in t1])

    full_normal_tiles = area(202298)
    full_inverted_tiles = area(202299)

    # print(total_possible_positions - odd*0)



if __name__ == "__main__":
    file = "demo.txt"
    if len(sys.argv) == 2:
        file = sys.argv[1]
    main(file)