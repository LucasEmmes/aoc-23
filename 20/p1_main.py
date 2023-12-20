from typing import Dict, List, Tuple
from dataclasses import dataclass
import sys
from copy import copy, deepcopy
import math

DEBUG = False

class Module:
    def __init__(self, name: str) -> None:
        self.outputs: List['Module'] = []
        self.name: str = name
        self.memories: List[Tuple[bool, str]] = []

    def trigger(self, signal: bool, src: str):
        self.memories.append((signal, src))

    def execute(self) -> (List['Module'], int):
        return []

    def __repr__(self) -> str:
        return f"{self.name} ({hex(id(self))})"

class Machine(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)
    
    def execute(self) -> (List['Module'], int):
        if self.memories.pop(0)[0] == False:
            return ([], -2)
        else:
            return ([], -1)
            

class Consumer(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)
    
    def execute(self) -> (List['Module'], int):
        return ([], -1)

class BroadCaster(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)
    
    def execute(self) -> (List['Module'], int):
        signal, _ = self.memories.pop(0)
        for module in self.outputs:
            module.trigger(signal, self.name)
            if DEBUG:
                print(f"broadcaster -low-> {module.name}")
        return (self.outputs, int(signal))

    def __repr__(self) -> str:
        if DEBUG:
            return f"[Broadcaster] -> ({[m.name for m in self.outputs]})"
        else:
            return Module.__repr__(self)

class FlipFlop(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.current_state: bool = False

    def execute(self) -> (List['Module'], int):
        signal, _ = self.memories.pop(0)
        if signal == True: return ([], -1)
        else:
            self.current_state = not self.current_state
            for module in self.outputs:
                module.trigger(self.current_state, self.name)
                if DEBUG:
                    print(f"{self.name} -{'high' if self.current_state else 'low'}-> {module.name}")
            return (self.outputs, int(self.current_state))
    
    def __repr__(self) -> str:
        if DEBUG:
            return f"[FlipFlop] {self.name}={self.current_state} -> ({[m.name for m in self.outputs]})"
        else:
            return Module.__repr__(self)

class Conjunction(Module):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.previous_inputs: Dict[str, bool] = {}

    def execute(self) -> List[Module]:
        signal, src = self.memories.pop(0)
        self.previous_inputs[src] = signal
        if sum(self.previous_inputs.values()) == len(self.previous_inputs):
            pulse = False
        else:
            pulse = True

        for module in self.outputs:
            module.trigger(pulse, self.name)
            if DEBUG:
                print(f"{self.name} -{'high' if pulse else 'low'}-> {module.name}")
        return (self.outputs, int(pulse))

    def __repr__(self) -> str:
        if DEBUG:
            return f"[Conjunction] {self.name}={self.previous_inputs} -> ({[m.name for m in self.outputs]})"
        else:
            return Module.__repr__(self)

def create_module(raw_string: str) -> Module:
    if raw_string == "broadcaster":
        return BroadCaster("broadcaster")
    elif raw_string.startswith("%"):
        return FlipFlop(raw_string[1:])
    elif raw_string.startswith("&"):
        return Conjunction(raw_string[1:])


def main(file):
    with open(file, "r") as f:
        lines = list(filter(lambda x: len(x) > 0, f.read().split("\n")))

    modules: Dict[str, Module] = {}

    # Pass 1, initialize empty modules
    for line in lines:
        left, _ = line.split(" -> ")
        module = create_module(left)
        modules[module.name] = module

    # Pass 2, link modules
    for line in lines:
        left, right = line.split(" -> ")
        left_name = left if left == "broadcaster" else left[1:]
        module = modules[left_name]

        right_names = right.split(", ")
        outputs: List[Module] = []
        for output_name in right_names:
            if output_name not in modules.keys():
                if output_name == "rx":
                    modules[output_name] = Machine("rx")
                if output_name == "output":
                    modules[output_name] = Consumer(output_name)
            output_module = modules[output_name]
            outputs.append(output_module)
            if type(output_module) == Conjunction:
                output_module.previous_inputs[module.name] = False
        module.outputs = outputs


    high = 0
    low = 0
    for _ in range(1000):
        low += 1
        broadcaster = modules["broadcaster"]
        broadcaster.trigger(False, "")
        triggered_modules, signal = broadcaster.execute()
        low += len(triggered_modules)
        queue: List[Module] = triggered_modules
        next_queue: List[Module] = []
        while len(queue) > 0:
            for module in queue:
                triggered_modules, signal = module.execute()
                next_queue += triggered_modules
                if signal==1: high += len(triggered_modules)
                elif signal==0: low += len(triggered_modules)
            queue = next_queue
            next_queue = []
    print(f"{low=}, {high=}")
    print(f"P1 {low*high}")


if __name__ == "__main__":
    file = "demo.txt"
    if len(sys.argv) > 1:
        file = sys.argv[1]
    if len(sys.argv) > 2:
        DEBUG = True
    main(file)