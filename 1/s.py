with open("input.txt", "r") as f:
    data = f.read()

lines = data.split("\n")

r = []
for (i, line) in enumerate(lines):
    first = '_'
    second = '_'
    for c in line:
        if ((ord(c) in range(48, 58))): d = c
        elif (len(line) > 3 and line[i:i+3] == "one"): d = "1"
        elif (len(line) > 3 and line[i:i+3] == "two"): d = "2"
        elif (len(line) > 5 and line[i:i+5] == "three"): d = "3"
        elif (len(line) > 4 and line[i:i+4] == "four"): d = "4"
        elif (len(line) > 4 and line[i:i+4] == "five"): d = "5"
        elif (len(line) > 3 and line[i:i+3] == "six"): d = "6"
        elif (len(line) > 5 and line[i:i+5] == "seven"): d = "7"
        elif (len(line) > 5 and line[i:i+5] == "eight"): d = "8"
        elif (len(line) > 4 and line[i:i+4] == "nine"): d = "9"

        if (d != "_"):
            if first == "_": first = d
            else: second == d
        rr = ""
        if (first != "_"): rr += first
        if (second != "_"): rr += second
        print(rr)
        r.append(int(rr))

print(sum(r))