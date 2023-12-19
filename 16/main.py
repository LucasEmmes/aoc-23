from typing import Dict, List, Tuple, Set, Deque
from collections import deque
import sys

def get_energized(mirs: List[List[str]], start: Tuple[int, int, int]):
    energized: Set[Tuple[int, int]] = set() # (y, x) of energized tiles
    beams: Deque[Tuple[int, int, int]] = deque([start]) # (y, x, direction) N=0, E=1, S=2, W=3
    btdt: Set[(int, int, int)] = set() # Check if we have been here before going in the same direction

    while len(beams) > 0:
        (y, x, direction) = beams.popleft()
        if (y, x, direction) in btdt:
            continue
        if direction == 0:
            ny = y - 1
            nx = x
            if ny >= 0:
                energized.add((ny, nx)) # next tile is energized
                
                if mirs[ny][nx] == "/":
                    beams.append((ny, nx, 1))
                elif mirs[ny][nx] == "\\":
                    beams.append((ny, nx, 3))
                elif mirs[ny][nx] == "-":
                    beams.append((ny, nx, 1))
                    beams.append((ny, nx, 3))
                else:
                    beams.append((ny, nx, direction))

        elif direction == 1:
            ny = y
            nx = x + 1
            if nx < len(mirs[0]):
                energized.add((ny, nx)) # next tile is energized
                
                if mirs[ny][nx] == "/":
                    beams.append((ny, nx, 0))
                elif mirs[ny][nx] == "\\":
                    beams.append((ny, nx, 2))
                elif mirs[ny][nx] == "|":
                    beams.append((ny, nx, 0))
                    beams.append((ny, nx, 2))
                else:
                    beams.append((ny, nx, direction))
        
        elif direction == 2:
            ny = y + 1
            nx = x
            if ny < len(mirs):
                energized.add((ny, nx)) # next tile is energized
                
                if mirs[ny][nx] == "/":
                    beams.append((ny, nx, 3))
                elif mirs[ny][nx] == "\\":
                    beams.append((ny, nx, 1))
                elif mirs[ny][nx] == "-":
                    beams.append((ny, nx, 1))
                    beams.append((ny, nx, 3))
                else:
                    beams.append((ny, nx, direction))

        elif direction == 3:
            ny = y
            nx = x - 1
            if nx >= 0:
                energized.add((ny, nx)) # next tile is energized
                
                if mirs[ny][nx] == "/":
                    beams.append((ny, nx, 2))
                elif mirs[ny][nx] == "\\":
                    beams.append((ny, nx, 0))
                elif mirs[ny][nx] == "|":
                    beams.append((ny, nx, 0))
                    beams.append((ny, nx, 2))
                else:
                    beams.append((ny, nx, direction))

        btdt.add((y, x, direction))

    return len(energized)

def main(file):
    with open(f"{file}.txt", "r") as f:
        lines = f.read().split("\n")[:-1]

    mirs: List[List[str]] = [[c for c in line] for line in lines]

    print(f"P1 {get_energized(mirs, (0, -1, 1))}")

    p2 = 0
    for x in range(0, mirs[0].__len__()):
        p2 = max(p2, get_energized(mirs, (-1, x, 2)))
        p2 = max(p2, get_energized(mirs, (mirs.__len__(), x, 0)))
    for y in range(0, mirs.__len__()):
        p2 = max(p2, get_energized(mirs, (y, -1, 1)))
        p2 = max(p2, get_energized(mirs, (y, mirs[0].__len__(), 3)))

    print(f"P2 {p2}")


if __name__ == "__main__":
    file = "demo.txt"
    if len(sys.argv) == 2:
        file = sys.argv[1]
    main(file)