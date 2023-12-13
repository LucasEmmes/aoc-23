def overlap_hor(a, b):
    x = min(len(a), len(b))
    for i in range(0,x):
        if a[i] != b[i]: return False
    return True

def overlap_vert(a, b):
    x = min(len(a), len(b))
    for i in range(0,x):
        if not overlap_hor(a[i], b[i]): return False
    return True

def main():
    with open("input.txt", "r") as f:
        sections = [i.split("\n") for i in f.read().split("\n\n")]

    p1 = 0
    for section in sections:
        hori = set([i for i in range(1,len(section[0])-1)])
        # check horizon
        for l, line in enumerate(section):
            hortemp = set()
            for i in range(1, line.__len__()):
                left = line[i-1::-1]
                right = line[i:]
                if overlap_hor(left, right):
                    hortemp.add(i)
            hori = hori.intersection(hortemp)
        if len(hori) > 1:
            print(f"FAILURE, HORI IS {hori}")
            exit()
        elif len(hori) == 1:
            p1 += hori.pop()
            continue

        # hor
        for i in range(1, section.__len__()-1):
            top = section[i-1::-1]
            bottom = section[i:]
            if overlap_vert(top, bottom):
                p1 += i*100
                continue
        
        print("FAILURE HELP NOTHING FOUND")

    print(f"P1 {p1}")


main()
    