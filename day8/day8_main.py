from __future__ import annotations
from dataclasses import dataclass
import re
from typing import List, Dict, Set

INPUT_PATH = "inp.txt"

@dataclass(frozen=True)
class DataPoint:
    x: int
    y: int

    @staticmethod
    def add(a: DataPoint, b: DataPoint) -> DataPoint:
        return DataPoint(x=a.x + b.x, y=a.y + b.y)
    
    @staticmethod
    def subtract(a: DataPoint, b: DataPoint) -> DataPoint:
        return DataPoint(x=a.x - b.x, y=a.y - b.y)

class Node:
    def __init__(self, val: DataPoint) -> None:
        self.value = val
        self.next = None

    def has_next(self) -> bool:
        return self.next is not None
    
    def set_next(self, to_set: Node) -> None:
        self.next = to_set

class LinkedList:
    def __init__(self, node_val: DataPoint) -> None:
        start = Node(node_val)
        self.start = start
        self._end = start

    def append(self, node_val: DataPoint) -> None:
        to_append = Node(node_val)
        self._end.set_next(to_append)
        self._end = to_append


def read_input(inp_path: str) -> List[str]:
    data = []
    with open(inp_path, "r", encoding="utf-8") as input_file:
        for line in input_file.readlines():
            line = line.strip()
            if not line:
                continue
            data.append(line)
    return data

def parse_data(data: List[str]) -> List[LinkedList]:
    rval: Dict[str, LinkedList] = {}
    for yval, line in enumerate(data):
        for freq_match in re.finditer(r"[a-zA-Z0-9]", line):
            pos = DataPoint(x=freq_match.start(), y=yval)
            freq = freq_match.group()
            if not freq in rval:
                rval[freq] = LinkedList(pos)
                continue
            rval[freq].append(pos)
    print(rval.keys())
    return [*rval.values()]

def get_valid_antinodes(pos: Node, xmax: int, ymax: int) -> Set[DataPoint]:
    if not pos.has_next():
        return set()
    valid = get_valid_antinodes(pos.next, xmax, ymax)
    
    slope_xmax = xmax/2
    slope_ymax = ymax/2
    comp = pos
    while comp.has_next():
        comp = comp.next
        slope = DataPoint.subtract(pos.value, comp.value)
        if abs(slope.x) >= slope_xmax:
            continue
        if abs(slope.y) >= slope_ymax:
            continue

        tmp = DataPoint.add(pos.value, slope)
        if 0 <= tmp.x < xmax and 0 <= tmp.y < ymax:
            valid.add(tmp)
        tmp = DataPoint.subtract(comp.value, slope)
        if 0 <= tmp.x <= xmax and 0 <= tmp.y < ymax:
            valid.add(tmp)
    return valid


def count_unique_antinodes(data: List[str]) -> int:
    total = set()
    xmax = len(data[0])
    ymax = len(data)
    print(xmax)
    print(ymax)
    freq_sets = parse_data(data)
    for freq in freq_sets:
        if freq.start.next is None:
            continue
        total.update(get_valid_antinodes(freq.start, xmax, ymax))
    for val in total:
        print(val)
    return len(total)

def main() -> None:
    """Script main function."""
    data = read_input(INPUT_PATH)
    print("Part I")
    print("-------")
    outp = count_unique_antinodes(data)
    print(f"Result: {outp}")
    print("======================")
    # print("Part II")
    # print("-------")
    # outp = count_distinct_loop_opportunities(room_map)
    # print(f"Result: {outp}")
    
if __name__ == "__main__":
    main()