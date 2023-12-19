from typing import Dict, List, Tuple
from dataclasses import dataclass
import sys
from copy import copy
import math

@dataclass
class MP:
    x: int
    m: int
    a: int
    s: int

def rule_creator(rule: str):
    attr = rule[0]
    cmp = rule[1]
    n = int(rule[2:])

    if attr == "x":
        get_attr = lambda mp: mp.x
    elif attr == "m":
        get_attr = lambda mp: mp.m
    elif attr == "a":
        get_attr = lambda mp: mp.a
    elif attr == "s":
        get_attr = lambda mp: mp.s
    
    if cmp == ">":
        return lambda mp: get_attr(mp) > n
    else:
        return lambda mp: get_attr(mp) < n


def main(file):
    with open(file, "r") as f:
        lines = list(filter(lambda x: len(x) > 0, f.read().split("\n")))



if __name__ == "__main__":
    file = "demo.txt"
    if len(sys.argv) == 2:
        file = sys.argv[1]
    main(file)