from typing import Dict, List, Tuple
from dataclasses import dataclass
import sys
from copy import copy, deepcopy
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
        return []
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
    union_list: List[range] = a.ranges + b.ranges
    return rangegroup_compress(RangeGroup(union_list))


def rangegroup_overlap(a: RangeGroup, b: RangeGroup) -> RangeGroup:
    overlap_list: List[range] = []
    for arange in a.ranges:
        for brange in b.ranges:
            overlap_list += range_overlap(arange, brange)
    return rangegroup_compress(RangeGroup(overlap_list))


def rangegroup_cut(a: RangeGroup, b: RangeGroup) -> RangeGroup:
    temp1 = []
    temp2 = a.ranges
    for brange in b.ranges:
        for r in temp2:
            overlap = range_overlap(r, brange)
            if len(overlap) > 0:
                overlap_region = overlap[0]
                if r.start < overlap_region.start:
                    temp1.append(range(r.start, overlap_region.start))
                if overlap_region.stop < r.stop:
                    temp1.append(range(overlap_region.stop, r.stop))
            else:
                temp1.append(r)
        temp2 = temp1
    return RangeGroup(temp2)

def workflow_overlap(a: WorkFlow, b: WorkFlow) -> WorkFlow:
    workflow: WorkFlow = [0,0,0,0]
    for i in range(4):
        workflow[i] = rangegroup_overlap(a[i], b[i])
    return workflow

def workflow_union(a: WorkFlow, b: WorkFlow) -> WorkFlow:
    workflow: WorkFlow = [0,0,0,0]
    for i in range(4):
        workflow[i] = rangegroup_union(a[i], b[i])
    return workflow

# workflow_str = qqz{s>2770:qs,m<1801:hdj,R}
# rules_string = s>2770:qs,m<1801:hdj
# rule_string = s>2770:qs

def split_raw_workflow(workflow_str: str) -> Tuple[str, List[str], str]:
    name, temp = workflow_str.split("{")
    rule_strings = temp[:-1].split(",")
    fallback = rule_strings.pop()
    return (name, rule_strings, fallback)

# def define_rule(rule_string: str, known_workflows: Dict[str, WorkFlow]) -> WorkFlow:
#     temp, destination_workflow = rule_string.split(":")
#     attr = temp[0]
#     cmp = temp[1]
#     val = int(temp[2:])

#     defined = [RangeGroup([range(0,4001)]), RangeGroup([range(0,4001)]), RangeGroup([range(0,4001)]), RangeGroup([range(0,4001)])]
#     i = "xmas".index(attr)

#     if cmp == "<":
#         defined[i].ranges = [range(0,val)]
#     else:
#         defined[i].ranges = [range(val+1, 4001)]

#     overlap = deepcopy(defined)
#     if destination_workflow == "R":
#         overlap = [RangeGroup([]), RangeGroup([]), RangeGroup([]), RangeGroup([])]
#     # If destination isn't A, check and do overlap
#     if destination_workflow in known_workflows.keys():
#         known = known_workflows[destination_workflow]
#         for i in range(4):
#             defined[i] = rangegroup_overlap(defined[i], known[i])
    
#     return defined
        


def is_fully_defined(rules_string: List[str], fallback: str, known_workflows: Dict[str, WorkFlow]) -> bool:
    # Check if fallback is invalid
    if fallback not in known_workflows.keys() and fallback not in "AR": return False
    # Check if any individual rule is invalid
    for rule_string in rules_string:
        destination_workflow_name = rule_string.split(":")[1]
        if destination_workflow_name not in known_workflows.keys() and destination_workflow_name not in "AR": return False
    return True

def define_workflow(rule_strings: List[str], fallback: str, known_workflows: Dict[str, WorkFlow]) -> RangeGroup:
    distributable = [RangeGroup([range(0,4001)]), RangeGroup([range(0,4001)]), RangeGroup([range(0,4001)]), RangeGroup([range(0,4001)])]
    defined_workflow = [RangeGroup([]), RangeGroup([]), RangeGroup([]), RangeGroup([])]

    for rule_string in rule_strings:
        temp, destination_name = rule_string.split(":")
        attr = temp[0]
        cmp = temp[1]
        val = int(temp[2:])
        i = "xmas".index(attr)

        if cmp == "<": rule = range(0, val)
        else: rule = range(val+1, 4001)

        if destination_name == "R":
            pass # nothing to do, just marking as thought of
        elif destination_name == "A":
            temp_workflow = [RangeGroup([range(0,4001)]), RangeGroup([range(0,4001)]), RangeGroup([range(0,4001)]), RangeGroup([range(0,4001)])]
            temp_workflow[i].ranges = [rule]
            overlap = workflow_overlap(temp_workflow, distributable)
            defined_workflow = workflow_union(defined_workflow, overlap)
        elif destination_name in known_workflows.keys():
            temp_workflow = [RangeGroup([range(0,4001)]), RangeGroup([range(0,4001)]), RangeGroup([range(0,4001)]), RangeGroup([range(0,4001)])]
            temp_workflow[i].ranges = [rule]
            overlap_1 = workflow_overlap(temp_workflow, known_workflows(destination_name))
            overlap_2 = workflow_overlap(overlap_1, distributable)
            defined_workflow = workflow_union(define_workflow, overlap_2)
        else:
            print("FAILURE, SHOULD HAVE FOUND DESTINATION IN known_workflows")
            exit()

        distributable[i] = rangegroup_cut(distributable[i], RangeGroup([rule]))
    
    if fallback == "R":
        pass # nothing to do, just marking as thought of
    elif fallback == "A":
        defined_workflow = workflow_union(defined_workflow, distributable)
    elif fallback in known_workflows.keys():
        overlap = workflow_overlap(distributable, known_workflows[fallback])
        defined_workflow = workflow_union(defined_workflow, overlap)
    else:
        print("FAILURE, SHOULD HAVE FOUND FALLBACK IN known_workflows")
        exit()

    return defined_workflow

def main(file):
    with open(file, "r") as f:
        lines = list(filter(lambda x: len(x) > 0, f.read().split("\n")))

    print(define_workflow(["s>2173:A","a>1545:R","m<3290:A"], "R", {}))

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
    cassert(range_overlap(a, b), [])

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

    # cut group --------------------------------------------
    a = RangeGroup([range(30,50)])
    b = RangeGroup([range(45,60)])
    cassert(rangegroup_cut(a, b).ranges, [range(30,45)])
    
    a = RangeGroup([range(30,50)])
    b = RangeGroup([range(60,65)])
    cassert(rangegroup_cut(a, b).ranges, [range(30,50)])

    a = RangeGroup([range(30,50)])
    b = RangeGroup([range(35,45)])
    cassert(rangegroup_cut(a, b).ranges, [range(30,35), range(45,50)])

if __name__ == "__main__":
    file = "demo.txt"
    if len(sys.argv) == 2:
        file = sys.argv[1]
    main(file)
    # testing()