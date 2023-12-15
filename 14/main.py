import copy
from functools import cache


def score(map):
    res = 0
    max = map.__len__()
    for i in range(0, max):
        for x in range(0, map[i].__len__()):
            if map[i][x] == 'O':
                res += max - i

    return res

def map2string(map):
    return "\n".join(["".join(line) for line in map])


memo_north = {}
def tilt_north(map):
    global memo_north
    mapstr = map2string(map)
    if mapstr in memo_north:
        return memo_north[mapstr]

    for i in range(map.__len__(), 1, -1):
        for y in range(1, i):
            for x in range(0, map[0].__len__()):
                if map[y][x] == 'O' and map[y-1][x] == '.':
                    map[y-1][x] = 'O'
                    map[y][x] = '.'
    memo_north[mapstr] = map.copy()
    return map

memo_south = {}
def tilt_south(map):
    global memo_south
    mapstr = map2string(map)
    if mapstr in memo_south:
        return memo_south[mapstr]
    
    for i in range(0, map.__len__()-1, 1):
        for y in range(map.__len__()-2, i-1, -1):
            for x in range(0, map[0].__len__()):
                if map[y][x] == 'O' and map[y+1][x] == '.':
                    map[y+1][x] = 'O'
                    map[y][x] = '.'
    memo_south[mapstr] = map.copy()
    return map

memo_east = {}
def tilt_east(map):
    global memo_east
    mapstr = map2string(map)
    if mapstr in memo_east:
        return memo_east[mapstr]
    
    for i in range(0, map[0].__len__()-1):
        for y in range(0, map.__len__()):
            for x in range(map[0].__len__()-2, i-1, -1):
                if map[y][x] == 'O' and map[y][x+1] == '.':
                    map[y][x+1] = 'O'
                    map[y][x] = '.'
    memo_east[mapstr] = map.copy()
    return map

memo_west = {}
def tilt_west(map):
    global memo_west
    mapstr = map2string(map)
    if mapstr in memo_west:
        return memo_west[mapstr]
    
    for i in range(map[0].__len__()-1, 0, -1):
        for y in range(0, map.__len__()):
            for x in range(0, map[0].__len__()):
                if map[y][x] == 'O' and map[y][x-1] == '.':
                    map[y][x-1] = 'O'
                    map[y][x] = '.'
    memo_west[mapstr] = map.copy()
    return map

def main():
    with open("demo.txt", "r") as f:
        lines = f.read().split("\n")
    lines.pop()

    map = [[c for c in line] for line in lines]
    original_map = map.copy()

    for i in range(1000000000):
        if i%1000000 == 0: print(i)
        map = tilt_north(map)
        map = tilt_west(map)
        map = tilt_south(map)
        map = tilt_east(map)

    print(score(map))
        

main()