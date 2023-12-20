from typing import Dict, List, Tuple
from dataclasses import dataclass
import sys
from copy import copy
import math

@dataclass
class RangeGroup:
    ranges: List[range]

WorkFlow = List[RangeGroup]

def range_union(a: range, b: range) -> List[range]:
    if (a.stop < b.start-1) or (b.stop < a.start-1):
        return [a, b]
    else:
        return [range(min(a.start, b.start), max(a.stop, b.stop))]


def range_overlap(a: range, b: range) -> List[range]:
    if (a.stop < b.start) or (b.stop < a.start):
        return [range(0,0)]
    else:
        return [range(max(a.start, b.start), min(a.stop, b.stop))]


def rangegroup_compress(group: RangeGroup) -> RangeGroup:
    if len(group.ranges) == 0: return group

    group.ranges.sort(key=lambda x: x.start)
    compressed: List[range] = []
    for r in group.ranges:
        if len(compressed) and compressed[-1].stop >= (r.start-1):
            compressed[-1] = range(compressed[-1].start, max(compressed[-1].stop, r.stop))
        else:
            compressed.append(r)
    for r in compressed[::-1]:
        if r.start == r.stop:
            compressed.remove(r)

    return RangeGroup(compressed)


def rangegroup_union(a: RangeGroup, b: RangeGroup) -> RangeGroup:
    union_list: List[range] = []
    for arange in a.ranges:
        for brange in b.ranges:
            union_list += range_union(arange, brange)
    return rangegroup_compress(RangeGroup(union_list))


def rangegroup_overlap(a: RangeGroup, b: RangeGroup) -> RangeGroup:
    overlap_list: List[range] = []
    for arange in a.ranges:
        for brange in b.ranges:
            overlap_list += range_overlap(arange, brange)
    return rangegroup_compress(RangeGroup(overlap_list))

# workflow_str = qqz{s>2770:qs,m<1801:hdj,R}
# rules_string = s>2770:qs,m<1801:hdj
# rule_string = s>2770:qs

def split_raw_workflow(workflow_str: str) -> Tuple[str, List[str], str]:
    pass

def is_fully_defined(rules_string: List[str], fallback: str, known_workflows: Dict[str, WorkFlow]) -> bool:
    # Check if fallback is invalid
    if fallback not in known_workflows.keys() and fallback not in "AR": return False
    # Check if any individual rule is invalid
    for rule_string in rules_string:
        destination_workflow_name = rule_string.split(":")[1]
        if destination_workflow_name not in known_workflows.keys() and destination_workflow_name not in "AR": return False
    return True

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

def main(file):
    with open(file, "r") as f:
        lines = list(filter(lambda x: len(x) > 0, f.read().split("\n")))



def cassert(a, b):
    if (a != b):
        print("Failed assertion!")
        print(f"Expected {b}\nbut was  {a}")
    
def testing():
    # union ------------------------------------------------------
    a = range(0,10)
    b = range(10,20)
    cassert(range_union(a, b), [range(0,20)])

    a = range(0,10)
    b = range(40,50)
    cassert(range_union(a, b), [range(0,10), range(40,50)])
    
    a = range(0,10)
    b = range(11,50)
    cassert(range_union(a, b), [range(0,50)])
    
    # overlap ------------------------------------------------------
    a = range(0,10)
    b = range(40,50)
    cassert(range_overlap(a, b), [range(0,0)])

    a = range(0,55)
    b = range(40,50)
    cassert(range_overlap(a, b), [range(40,50)])
    
    a = range(0,55)
    b = range(40,60)
    cassert(range_overlap(a, b), [range(40,55)])

    # compress group --------------------------------------------
    a = RangeGroup([range(10,40), range(0,5), range(30,50), range(0,2)])
    cassert(rangegroup_compress(a).ranges, [range(0,5), range(10,50)])

    a = RangeGroup([range(0,10), range(51,55), range(11, 50)])
    cassert(rangegroup_compress(a).ranges, [range(0,55)])

    # union group --------------------------------------------
    a = RangeGroup([range(0,40), range(50,60)])
    b = RangeGroup([range(40,50), range(50,60)])
    cassert(rangegroup_union(a, b).ranges, [range(0,60)])

    a = RangeGroup([range(0,40), range(100,160)])
    b = RangeGroup([range(30,45), range(0,5), range(55,60)])
    cassert(rangegroup_union(a, b).ranges, [range(0,45), range(55,60), range(100,160)])
    
    # overlap group --------------------------------------------
    a = RangeGroup([range(0,40), range(50,60)])
    b = RangeGroup([range(40,50), range(50,60)])
    cassert(rangegroup_overlap(a, b).ranges, [range(50,60)])

    a = RangeGroup([range(0,40), range(100,160)])
    b = RangeGroup([range(50,55), range(0,5), range(55,60)])
    cassert(rangegroup_overlap(a, b).ranges, [range(0,5)])



if __name__ == "__main__":
    file = "demo.txt"
    if len(sys.argv) == 2:
        file = sys.argv[1]
    # main(file)
    testing()