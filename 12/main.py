from typing import List, Tuple, Dict
import json

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

def partial_check_pattern(input_str: str, values: List[int]) -> bool:
    check = []
    squares = 0
    jokers = 0
    guaranteed_values = 0
    for c in input_str:
        if c == "#":
            squares += 1
        elif c == "?":
            jokers += 1
        else:
            if squares != 0:
                check.append(range(squares,squares+jokers+1))
                squares = 0
                jokers = 0
    if squares != 0:
        check.append(range(squares, squares+jokers+1))

    if len(check) < len(values): return True
    elif len(check) > len(values): return False
    else:
        for a, b in zip(values, check):
            if a not in b: return False
    
    return True

def apply_mask(input_str: str, mask: List[str]) -> str:
    res = []
    mask.reverse()
    for i in input_str:
        if i == "?":
            res.append(mask.pop())
        else:
            res.append(i)

    return "".join(res)

def get_range(segment: str) -> Dict[List[int], int]:
    res = {}
    jokers = segment.count("?")
    for i in range(0, 2**jokers):
        mask = ["#" if i=="1" else "." for i in bin(i)[2:].rjust(jokers, "0")]
        masked_segment = apply_mask(segment, mask)
        temp = tuple(filter(lambda x: x > 0, [len(s) for s in masked_segment.split(".")]))
        # if len(temp) > 0:
        if temp not in res:
            res[temp] = 0
        res[temp] += 1
    return res

def permutations_bruh(elements):
    if len(elements) == 1:
        return elements[0]
    
    perms = []
    for el in elements[0]:
        for step in permutations_bruh(elements[1:]):
            perms.append(el+step)
    return perms

def permutations(segments: List[str], data: Dict[str, List[Tuple[Tuple[int], int]]]) -> List[Tuple[List[int], int]]:
    if len(segments) == 1:
        return data[segments[0]]

    perms = []
    for (possible_view, score) in data[segments[0]]:
        for (step_view, step_score) in permutations(segments[1:], data):
            perms.append(tuple([possible_view + step_view, score*step_score]))
    return perms

def count_matching_permutations(value: List[int], segments: List[str], data: Dict[str, List[Tuple[Tuple[int], int]]], current: List[int] = []) -> int:
    if len(segments) == 0:
        if value == current: return 1
        else: return 0

    p = 0
    for tup, score in data[segments[0]]:
        temp = current + list(tup)
        if len(temp)<=len(value) and temp == value[0:len(temp)]:
            p += count_matching_permutations(value, segments[1:], data, temp)*score
    return p


def main():
    with open("demo.txt", "r") as f:
        lines = f.read().split("\n")
    lines.pop()

    p1 = 0
    memo: Dict[str, List[Tuple[Tuple(int), int]]] = {}
    for linecount, line in enumerate(lines):
        if linecount%1 == 0: print(f"Line {linecount}")
        
        # Split line into input and value
        input_str, values = line.split(" ")
        
        # Note down number of segments before and after multiplication
        # segments_p1 = list(filter(lambda x: len(x) > 0, input_str.split(".")))
        input_str = "?".join([input_str]*5)
        segments_p2 = list(filter(lambda x: len(x) > 0, input_str.split(".")))

        # Multiply values, then split
        values = ",".join([values]*5)
        values = [int(i) for i in values.split(",")]

        for segment in segments_p2:
            if segment not in memo:
                memo[segment] = list(get_range(segment).items())
        p1 += count_matching_permutations(values, segments_p2, memo, [])
        
        # for (perm_view, perm_score) in permutations(segments, memo):
        #     if list(perm_view) == values:
        #         p1 += perm_score
    print(p1)






    # PART 1 NEW

    # p1 = 0
    # memo: Dict[str, List[Tuple[Tuple(int), int]]] = {}
    # for linecount, line in enumerate(lines):
    #     if linecount%1 == 0: print(f"Line {linecount}")
    #     input_str, values = line.split(" ")
    #     input_str = "?".join([input_str]*5)
    #     values = ",".join([values]*5)
    #     values = [int(i) for i in values.split(",")]
    #     segments = list(filter(lambda x: len(x) > 0, input_str.split(".")))
    #     for segment in segments:
    #         if segment not in memo:
    #             memo[segment] = list(get_range(segment).items())
    #     for (perm_view, perm_score) in permutations(segments, memo):
    #         if list(perm_view) == values:
    #             p1 += perm_score
    # print(p1)






    # PART 1 OLD

    # p1 = 0
    # line_perms = {}
    # for linecount, line in enumerate(lines):
    #     line_perms[linecount] = 0
    #     if linecount%50 == 0: print(linecount)
    #     input_str, values = line.split(" ")
    #     values = [int(i) for i in values.split(",")]
    #     jokers = input_str.count("?")
    #     for i in range(0, 2**jokers):
    #         mask = ["#" if i=="1" else "." for i in bin(i)[2:].rjust(jokers, "0")]
    #         input_copy = apply_mask(input_str, mask)
    #         if check_pattern(input_copy, values):
    #             p1 += 1
    #             line_perms[linecount] += 1
    
    # with open("valid.txt", "w") as f:
    #     f.write(f"{json.dumps(line_perms)}")
    
    # print(p1)



        



if __name__ == "__main__": main()