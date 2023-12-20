a = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}"""

def completely_defined(input) -> bool:
    rule_name, rules_raw = input.split("{")
    rule_strings = rules_raw[:-1].split(",")
    fallback = rule_strings.pop()

    if fallback not in "AR": return False

    for rule_string in rule_strings:
        _, value = rule_string.split(":")
        if value not in "AR": return False

    return True

def get_range(rule: str):
    attr = rule[0]
    cmp = rule[1]
    n = int(rule[2:])

    ranges = [range(0,4001), range(0,4001), range(0,4001), range(0,4001)]
    i = "xmas".index(attr)
    if cmp == ">":
        ranges[i] = range(n+1, 4001)
    else:
        ranges[i] = range(0, n)
    
    return ranges

# for line in a.split("\n"):
#     print(completely_defined(line))

print(get_range("x<2561"))
print(get_range("a>200"))