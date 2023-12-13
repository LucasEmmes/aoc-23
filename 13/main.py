from typing import List, Dict, Tuple

def get_diffs(a: List[List[str]], b: List[List[str]]) -> bool:
    diffs = 0
    m = min(len(a), len(b))
    for i in range(0, m):
        for j in range(0, len(a[i])):
            if a[i][j] != b[i][j]: diffs += 1
    return diffs

def main():
    with open("input.txt", "r") as f:
        sections: List[str] = f.read().split("\n\n")

    # Parsing
    sections_p1: List[List[List[str]]] = []
    sections_p2: List[List[List[str]]] = []
    for (sec_num, section) in enumerate(sections):
        lines = list(filter(lambda x: len(x) > 0, section.split("\n")))
        
        temp_p1_full: List[List[str]] = []
        temp_p2_full: List[List[str]] = []
        for _ in range(0, lines[0].__len__()):
            temp_p2_full.append([])

        for y in range(0, lines.__len__()):
            temp_p1_row = []
            for x in range(0, lines[0].__len__()):
                temp_p1_row.append(lines[y][x])
                temp_p2_full[x].insert(0, lines[y][x])
            temp_p1_full.append(temp_p1_row)

        sections_p1.append(temp_p1_full)
        sections_p2.append(temp_p2_full)

    # Checking
    p1 = 0
    
    for (section_num, (section_hor, section_ver)) in enumerate(zip(sections_p1, sections_p2)):
        found = False
        # Check horizontal
        for i in range(1, len(section_hor)):
            top = section_hor[i-1::-1]
            bottom = section_hor[i::]
            if get_diffs(top, bottom) == 0:
                p1 += i*100
                found = True
                break
        
        if found: continue

        # Check vertical
        for i in range(1, len(section_ver)):
            top = section_ver[i-1::-1]
            bottom = section_ver[i::]
            if get_diffs(top, bottom) == 0:
                p1 += i
                found = True
                break
        
        if not found: print(f"Failed section {section_num}")

    print(f"P1 {p1}")


    p2 = 0

    for (section_num, (section_hor, section_ver)) in enumerate(zip(sections_p1, sections_p2)):
        found = False
        # Check horizontal
        for i in range(1, len(section_hor)):
            top = section_hor[i-1::-1]
            bottom = section_hor[i::]
            if get_diffs(top, bottom) == 1:
                p2 += i*100
                found = True
                break
        
        if found: continue

        # Check vertical
        for i in range(1, len(section_ver)):
            top = section_ver[i-1::-1]
            bottom = section_ver[i::]
            if get_diffs(top, bottom) == 1:
                p2 += i
                found = True
                break
        
        if not found: print(f"Failed section {section_num}")

    print(f"P2 {p2}")




main()
    