from typing import Dict, List

def h(section):
    temp = 0
    for c in section:
        temp += ord(c)
        temp = temp*17
        temp = temp%256
    return temp

def main():
    with open("input.txt", "r") as f:
        lines = f.read().split("\n")
    lines.pop()

    p1 = 0

    for section in lines[0].split(","):
        p1 += h(section)

    print(f"P1 {p1}")


    d: Dict[int, List[str]] = {}
    for i in range(0, 256):
        d[i] = []

    for section in lines[0].split(","):
        if (section.split("-").__len__() == 2):
            lens = section.split("-")[0]
            box = h(lens)
            for i in range(0, d[box].__len__()):
                if d[box][i].startswith(lens):
                    d[box] = d[box][:i] + d[box][i+1:]
                    break
        else:
            lens, focallength = section.split("=")
            box = h(lens)
            found = False
            for i in range(0, d[box].__len__()):
                if d[box][i].startswith(lens):
                    d[box][i] = section
                    found = True
                    break
            if not found:
                d[box].append(section)

    p2 = 0
    for i in range(0, 256):
        for j in range(0, d[i].__len__()):
            p2 += (i+1) * (j+1) * int(d[i][j].split("=")[1])
        
    print(f"P2 {p2}")
        

main()