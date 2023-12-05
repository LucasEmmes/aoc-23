def main():
    with open("input.txt", "r") as f :
        raw = f.read()

    sections = raw.split("\n\n")

    seeds = sections[0]
    seeds = [int(i) for i in seeds.split(" ")[1:]]

    seeds = [[seeds[i], seeds[i]+seeds[i+1]] for i in range(0, seeds.__len__(), 2)]

    maps = {}

    current_line = []
    for section in sections[1:]:
        for line in section.split("\n"):
            if line == "": continue
            if "map" in line:
                current_line = []
                maps[line] = current_line
            else:
                t, f, r = [int(i) for i in line.split(" ")]
                current_line.append([[f, f+r], [t, t+r]])
        
    for (k, v) in maps.items():
        print(v)
        v = sorted(v, key=lambda x: x[0])
        pre_len = v.__len__()
        for i in range(0, pre_len, -1):
            space = v[i+1][0][0] - v[i][0][1]
            if space > 1:
                v.append([[v[i][0][1]+1, v[i][0][1]+space], [v[i][0][1]+1, v[i][0][1]+space]])
        v = sorted(v, key=lambda x: x[0])
        print(v)
        exit()

    for seed_range in seeds:
        for map_range in maps["seed-to-soil map:"]:
            print(map_range)


main()

def overlap(a, b):
    start = max(a[0], b[0])
    end = min(a[1], b[1])
    if (start <= end):
        return [start, end]
    else:
        return None
    
