
def can_make(segment: str, )

def main():
    with open("demo.txt", "r") as f:
        lines = f.read().split("\n")
    lines.pop()

    for linecount, line in enumerate(lines):
        if linecount%1 == 0: print(f"Line {linecount}")
        
        # Split line into input and value
        segments_str, values_str = line.split(" ")
        segments = list(filter(lambda x: len(x) > 0, segments_str.split(".")))
        values = [int(i) for i in values_str.split(",")]





if __name__ == "__main__": main()