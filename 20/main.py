from typing import Dict, List, Tuple
from dataclasses import dataclass
import sys
from copy import copy
import math

class Module:
    def __init__(self, name: str) -> None:
        self.output: List['Module'] = []
        self.name: str = name

    def trigger(self, signal: bool, src: str) -> List['Module']:
        pass


class BroadCaster(Module):
    def __init__(self, name: str) -> None:
        Module.__init__(self, name)
    
    def trigger(self, signal: bool, src: str) -> List['Module']:
        for module in self.output:
            module.trigger(signal, self.name)
        return self.output
    

class FlipFlop(Module):
    def __init__(self, name: str) -> None:
        Module.__init__(self, name)
        self.current_state: bool = False

    def trigger(self, signal: bool, src: str) -> List['Module']:
        if signal == True: return []
        else:
            self.current_state = not self.current_state
            for module in self.output:
                module.trigger(self.current_state, self.name)
            return self.output


class Conjunction(Module):
    def __init__(self, name: str) -> None:
        Module.__init__(self, name)
        self.previous_inputs: Dict[str, bool]

    def trigger(self, signal: bool, src: str) -> List[Module]:
        self.previous_inputs[src] = signal
        if sum(self.previous_inputs.values()) == len(self.previous_inputs):
            pulse = False
        else:
            pulse = True

        for module in self.output:
            module.trigger(pulse, self.name)
        return self.output

def create_module(raw_string: str) -> Module:
    if raw_string.startswith("broadcaster"):
        return BroadCaster("broadcaster")
    elif raw_string.startswith("%"):
        return FlipFlop(raw_string[1:])
    elif raw_string.startswith("&"):
        return Conjunction(raw_string[1:])

def main(file):
    with open(file, "r") as f:
        lines = list(filter(lambda x: len(x) > 0, f.read().split("\n")))

    modules: Dict[Module] = {}

    for line in lines:
        left, right = line.split(" -> ")
        temp = create_module(left)
        modules[temp.name] = temp



if __name__ == "__main__":
    file = "demo.txt"
    if len(sys.argv) == 2:
        file = sys.argv[1]
    main(file)