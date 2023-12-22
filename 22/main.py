from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
import sys
from copy import copy, deepcopy
import math

@dataclass(frozen=True)
class Position:
    x: int
    y: int
    z: int

@dataclass
class Brick:
    def __init__(self, p1, p2) -> None:
        self.start: Position = p1 # start coord. the ned that has lower x, y, or z value
        self.end: Position = p2  # end coord
        self.supported_by: Set[str] = set()

        self.orientation = 0   # default if just one cube
        # 0 = x diff, 1 = y diff, 2 = z diff
        if self.start.x < self.end.x:
            self.orientation = 1
        elif self.start.y < self.end.y:
            self.orientation = 2
        elif self.start.z < self.end.z:
            self.orientation = 3

        self.name = ""
    
    def __repr__(self) -> str:
        if self.name != "": return f"[{self.name}] {self.start} ~ {self.end}"
        return f"{self.start} ~ {self.end}"

    def get_cubes(self: 'Brick') -> List[Position]:
        result = []
        if self.orientation == 0:
            return [self.start]
        elif self.orientation == 1:
            for x in range(self.start.x, self.end.x+1):
                result.append(Position(x, self.start.y, self.start.z))
        elif self.orientation == 2:
            for y in range(self.start.y, self.end.y+1):
                result.append(Position(self.start.x, y, self.start.z))
        elif self.orientation == 3:
            for z in range(self.start.z, self.end.z+1):
                result.append(Position(self.start.x, self.start.y, z))
        return result
    
    def get_down(self: 'Brick') -> 'Brick':
        return Brick(Position(self.start.x, self.start.y, self.start.z-1), Position(self.end.x, self.end.y, self.end.z-1))
    
    def get_up(self: 'Brick') -> 'Brick':
        return Brick(Position(self.start.x, self.start.y, self.start.z+1), Position(self.end.x, self.end.y, self.end.z+1))
    
    def __eq__(self, other: 'Brick') -> bool:
        return self.start == other.start and self.end == other.end

    def __gt__(self, other: 'Brick') -> bool:
        return self.start.z > other.start.z

    def __sub__(self, other: 'Brick') -> Set[Position]:
        own_cubes = set(self.get_cubes())
        other_cubes = set(other.get_cubes())
        return own_cubes - other_cubes
    
bricklist: List[Brick] = []
bricks_dic: Dict[str, Brick] = {}
occupied_space: Dict[Position, Brick] = {}

def number_of_supported(bricks: List[Brick], fallen_bricks: Set[str] = set()) -> int:
    all_supported_cubes: Set[Position] = set()
    brick_names: Set[str] = set([brick.name for brick in bricks])
    all_completely_supported_brick_names: Set[str] = set()
    previously_fallen = brick_names.union(fallen_bricks)

    # Collect complete list of all potentially supported cubes
    for brick in bricks:
        supported_cubes = brick.get_up() - brick
        all_supported_cubes = all_supported_cubes.union(supported_cubes)

    # Check which ones actually support other bricks, and if we are the only ones
    for cube in all_supported_cubes:
        if cube in occupied_space.keys():
            supported_brick = occupied_space[cube]
            if supported_brick.supported_by - previously_fallen == set():
                all_completely_supported_brick_names.add(supported_brick.name)
    
    all_completely_supported_bricks = [bricks_dic[name] for name in all_completely_supported_brick_names]
    
    if len(all_completely_supported_brick_names) == 0:
        return 0
    else:
        return len(all_completely_supported_brick_names) + number_of_supported(all_completely_supported_bricks, previously_fallen)

def main(file):
    with open(file, "r") as f:
        lines = list(filter(lambda x: len(x) > 0, f.read().split("\n")))

    names = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    global bricks_dic
    global bricklist
    global occupied_space
    # occupied_space: Set[Position] = set()
    

    for i, line in enumerate(lines):
        left, right = line.split("~")
        lx, ly, lz = [int(i) for i in left.split(",")]
        rx, ry, rz = [int(i) for i in right.split(",")]
        new_brick = Brick(Position(lx, ly, lz), Position(rx, ry, rz))
        # new_brick.name = names[i]
        new_brick.name = str(i)
        bricks_dic[str(i)] = new_brick
        bricklist.append(new_brick)
        for cube in new_brick.get_cubes():
            # occupied_space.add(cube)
            occupied_space[cube] = new_brick

    all_landed = False
    while all_landed != True:
        all_landed = True
        bricklist.sort()

        for brick in bricklist:
            if brick.start.z == 1: continue

            can_move_down = True
            while can_move_down and brick.start.z > 1:
                brick_moved_down = brick.get_down()
                space_diff = brick_moved_down - brick
                
                for cube in space_diff:
                    # if cube in occupied_space:
                    if cube in occupied_space.keys():
                        can_move_down = False
                        break
                
                if can_move_down:
                    # print(f"Moving down {brick}")
                    all_landed = False
                    for c in brick_moved_down - brick:
                        # occupied_space.add(c)
                        occupied_space[c] = brick
                    for c in brick - brick_moved_down:
                        # occupied_space.remove(c)
                        del occupied_space[c]
                    brick.start = brick_moved_down.start
                    brick.end = brick_moved_down.end

    # count
    for brick in bricklist:
        cubes_above = brick.get_up() - brick
        for cube in cubes_above:
            # if cube in occupied_space:
            if cube in occupied_space.keys():
                occupied_space[cube].supported_by.add(brick.name)
                # print(f"{brick.name} supports {occupied_space[cube].name}")
    
    # print()
    can_be_disintegrated: Set[str] = set()
    for brick in bricklist:
        if len(brick.supported_by) > 1:
            # print(f"{brick.name} is supported by {brick.supported_by}")
            for name in brick.supported_by:
                can_be_disintegrated.add(name)

    for brick in bricklist:
        if len(brick.supported_by) == 1:
            for name in brick.supported_by:
                # print(f"{name} is only support of {brick.name}")
                if name in can_be_disintegrated:
                    can_be_disintegrated.remove(name)

    for brick in bricklist:
        doesnt_support = True
        for cube in brick.get_up() - brick:
            if cube in occupied_space.keys():
                doesnt_support = False
                break
        if doesnt_support:
            # print(f"{brick.name} doesn't support any other bricks")
            can_be_disintegrated.add(brick.name)

    # P1
    print(f"P1 {len(can_be_disintegrated)}")

    # P2
    p2 = 0
    for brick in bricklist:
        if brick.name in can_be_disintegrated: continue
        p2 += number_of_supported([brick])
    print(f"P2 {p2}")
    
        


if __name__ == "__main__":
    file = "demo.txt"
    if len(sys.argv) == 2:
        file = sys.argv[1]
    main(file)