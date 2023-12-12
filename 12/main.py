from typing import List, Tuple, Dict

def check_pattern(input_str: str, values: List[int]) -> bool:
    check = []
    cont = 0
    for c in input_str:
        if c == "#":
            cont += 1
        else:
            if cont != 0:
                check.append(cont)
                cont = 0
    if cont != 0:
        check.append(cont)
    return check == values

def get_indeces(input_str: str) -> List[int]:
    indeces = []
    for (i, c) in enumerate(input_str):
        if c == "?":
            indeces.append(i)

    return indeces

def apply_mask(input_str: str, mask: List[str]) -> str:
    res = []
    mask.reverse()
    for i in input_str:
        if i == "?":
            res.append(mask.pop())
        else:
            res.append(i)

    return "".join(res)

def main():
    with open("input.txt", "r") as f:
        lines = f.read().split("\n")
    lines.pop()

    p1 = 0
    for linecount, line in enumerate(lines):
        print(linecount)
        input_str, values = line.split(" ")
        values = [int(i) for i in values.split(",")]
        jokers = input_str.count("?")
        for i in range(0, 2**jokers):
            mask = ["#" if i=="1" else "." for i in bin(i)[2:].rjust(jokers, "0")]
            input_copy = apply_mask(input_str, mask)
            if check_pattern(input_copy, values):
                p1 += 1
    
    print(p1)
        
    



if __name__ == "__main__": main()