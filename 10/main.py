from dataclasses import dataclass
from typing import Dict, Tuple, List, Set
import math

@dataclass
class Pipe:
    type: str
    pos: Tuple[int, int]
    one: Tuple[int, int]
    two: Tuple[int, int]

def is_loop(pipe: Pipe, pipes: Dict[Tuple[int, int], Pipe]) -> Tuple[bool, int]:
    start = pipe
    previous = None
    counter = 0

    while pipe.one in pipes and pipe.two in pipes:
        if  pipe.one in pipes and \
            pipes[pipe.one] != previous and \
            (pipes[pipe.two] == previous or previous == None):

            previous = pipe
            pipe = pipes[pipe.one]
        elif    pipe.two in pipes and \
                pipes[pipe.two] != previous and \
                (pipes[pipe.one] == previous or previous == None):
            
            previous = pipe
            pipe = pipes[pipe.two]
        else:
            return (False, counter)
        
        counter += 1
    
        if pipe == start and previous != None:
            return (True, counter)
    
    return (False, counter)

def make_list(pipe: Pipe, pipes: Dict[Tuple[int, int], Pipe]) -> List[Tuple[int, int]]:
    if is_loop(pipe, pipes)[0] == False: return []
    
    start = pipe
    previous = None
    counter = 0

    res = []

    while pipe.one in pipes and pipe.two in pipes:
        if  pipe.one in pipes and \
            pipes[pipe.one] != previous and \
            (pipes[pipe.two] == previous or previous == None):
            
            res.append(pipe.one)
            previous = pipe
            pipe = pipes[pipe.one]
        elif    pipe.two in pipes and \
                pipes[pipe.two] != previous and \
                (pipes[pipe.one] == previous or previous == None):
            
            res.append(pipe.two)
            previous = pipe
            pipe = pipes[pipe.two]
        
        counter += 1
    
        if pipe == start and previous != None:
            return res


def main():
    with open("input.txt", "r") as f:
        lines = f.read().split("\n")
    lines.pop()
    
    lines.insert(0, "."*lines[0].__len__())
    lines.append("."*lines[0].__len__())
    for i in range(0, lines.__len__()):
        lines[i] = "." + lines[i] + "."

    map = [list(i) for i in lines]

    WIDTH = map[0].__len__()
    HEIGHT = map.__len__()

    pipes: Dict[Tuple[int, int], Pipe] = {}

    for y in range(0,map.__len__()):
        for x in range(0,map[0].__len__()):
            if map[y][x] in ["|", "-", "L", "J", "7", "F"]:
                pipes[(y, x)] = Pipe(map[y][x], (y, x), None, None)
            if map[y][x] == "S":
                start = (y, x)
    
    y, x = start
    pipes[start] = Pipe("|", start, None, None)

    # link pipes
    for k, v, in pipes.items():
        y, x = k

        if v.type == "|":
            if map[y-1][x] in ["|", "F", "7", "S"]:
                v.one = (y-1, x)
            if map[y+1][x] in ["|", "J", "L", "S"]:
                v.two = (y+1, x)

        if v.type == "-":
            if map[y][x+1] in ["-", "J", "7"]:
                v.one = (y, x+1)
            if map[y][x-1] in ["-", "F", "L"]:
                v.two = (y, x-1)

        if v.type == "J":
            if map[y-1][x] in ["|", "F", "7", "S"]:
                v.one = (y-1, x)
            if map[y][x-1] in ["-", "F", "L"]:
                v.two = (y, x-1)

        if v.type == "L":
            if map[y-1][x] in ["|", "F", "7", "S"]:
                v.one = (y-1, x)
            if map[y][x+1] in ["-", "J", "7"]:
                v.two = (y, x+1)

        if v.type == "7":
            if map[y][x-1] in ["-", "F", "L"]:
                v.one = (y, x-1)
            if map[y+1][x] in ["|", "J", "L", "S"]:
                v.two = (y+1, x)

        if v.type == "F":
            if map[y][x+1] in ["-", "J", "7"]:
                v.one = (y, x+1)
            if map[y+1][x] in ["|", "J", "L", "S"]:
                v.two = (y+1, x)
        pipes[(y, x)] = v

    _, length = is_loop(pipes[start], pipes)
    print(f"P1 {math.floor(length/2)}")

    loop = make_list(pipes[start], pipes)
    
    enclosed_tiles: Set[Tuple[int, int]] = set()
    for i, tile in enumerate(loop):
        sy, sx = tile
        if (i%100==0): print(f"{i} / {loop.__len__()}")
        # DOWN
        temp_tiles = set()
        stop = False
        temp_counter = 0
        came_from = None
        for y in range(sy+1, HEIGHT):
            if (y, sx) in loop and pipes[(y, sx)].type != "|":
                if pipes[(y, sx)].type == "-":
                    stop = True
                    temp_counter+=1
                    came_from = None
                if pipes[(y, sx)].type == "L" or pipes[(y, sx)].type == "F":
                    if came_from == "left":
                        came_from == None
                        stop = True
                        temp_counter+=1
                    elif came_from == None:
                        came_from = "right"
                if pipes[(y, sx)].type == "7" or pipes[(y, sx)].type == "J":
                    if came_from == "right":
                        came_from == None
                        stop = True
                        temp_counter+=1
                    elif came_from == None:
                        came_from = "left"
            elif (not stop) and (y, sx) not in loop:
                    temp_tiles.add((y, sx))
        if temp_counter%2 == 1:
            enclosed_tiles = enclosed_tiles.union(temp_tiles)
        
        # UP
        temp_tiles = set()
        stop = False
        temp_counter = 0
        came_from = None
        for y in range(sy-1, 0, -1):
            if (y, sx) in loop and pipes[(y, sx)].type != "|":
                if pipes[(y, sx)].type == "-":
                    stop = True
                    temp_counter+=1
                    came_from = None
                if pipes[(y, sx)].type == "L" or pipes[(y, sx)].type == "F":
                    if came_from == "left":
                        came_from == None
                        stop = True
                        temp_counter+=1
                    elif came_from == None:
                        came_from = "right"
                if pipes[(y, sx)].type == "7" or pipes[(y, sx)].type == "J":
                    if came_from == "right":
                        came_from == None
                        stop = True
                        temp_counter+=1
                    elif came_from == None:
                        came_from = "left"

            elif (not stop) and (y, sx) not in loop:
                    temp_tiles.add((y, sx))
        if temp_counter%2 == 1:
            enclosed_tiles = enclosed_tiles.union(temp_tiles)
        
        # RIGHT
        temp_tiles = set()
        stop = False
        temp_counter = 0
        came_from = None
        for x in range(sx+1, WIDTH):
            if (sy, x) in loop and pipes[(sy, x)].type != "-":
                if pipes[(sy, x)].type == "|":
                    stop = True
                    temp_counter+=1
                    came_from = None
                if pipes[(sy, x)].type == "7" or pipes[(sy, x)].type == "F":
                    if came_from == "top":
                        came_from == None
                        stop = True
                        temp_counter+=1
                    elif came_from == None:
                        came_from = "bottom"
                if pipes[(sy, x)].type == "L" or pipes[(sy, x)].type == "J":
                    if came_from == "bottom":
                        came_from == None
                        stop = True
                        temp_counter+=1
                    elif came_from == None:
                        came_from = "top"
            elif (not stop) and (sy, x) not in loop:
                    temp_tiles.add((sy, x))
        if temp_counter%2 == 1:
            enclosed_tiles = enclosed_tiles.union(temp_tiles)
        
        # LEFT
        temp_tiles = set()
        stop = False
        temp_counter = 0
        came_from = None
        for x in range(sx-1, 0, -1):
            if (sy, x) in loop and pipes[(sy, x)].type != "-":
                if pipes[(sy, x)].type == "|":
                    stop = True
                    temp_counter+=1
                    came_from = None
                if pipes[(sy, x)].type == "7" or pipes[(sy, x)].type == "F":
                    if came_from == "top":
                        came_from == None
                        stop = True
                        temp_counter+=1
                    elif came_from == None:
                        came_from = "bottom"
                if pipes[(sy, x)].type == "L" or pipes[(sy, x)].type == "J":
                    if came_from == "bottom":
                        came_from == None
                        stop = True
                        temp_counter+=1
                    elif came_from == None:
                        came_from = "top"
            elif (not stop) and (sy, x) not in loop:
                    temp_tiles.add((sy, x))
        if temp_counter%2 == 1:
            enclosed_tiles = enclosed_tiles.union(temp_tiles)

    print(f"P2 {len(enclosed_tiles)}")

    # for y in range(0, HEIGHT):
    #     for x in range(0, WIDTH):
    #         if (y, x) in enclosed_tiles and (y, x) in loop:
    #             print("█", end="")
    #         elif (y, x) in enclosed_tiles:
    #             print("I", end="")
    #         elif (y, x) in loop:
    #             print("#", end="")
    #         else:
    #             print(".", end="")
    #     print()

if __name__ == "__main__":
    main()