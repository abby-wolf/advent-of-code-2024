from typing import List, Tuple
import time
from collections import Counter

INPUT_PATH = "inp.txt"

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

DIR_MAP = [(-1, 0), (0, 1), (1, 0), (0, -1)]

EMPTY_SPACE = "."
BLOCKED_SPACE = "#"
START_UP = "^"
START_LEFT = ">"
START_RIGHT = "<"

def read_input(inp_path: str) -> List[str]:
    """Read the input data.
    
    Parameters
    ----------
    inp_path : str
        Input data filepath.
    
    Returns
    -------
    List[str]
        The input data.
    
    """
    data = []
    with open(inp_path, "r", encoding="utf-8") as input_file:
        for line in input_file.readlines():
            if not line:
                continue
            data.append(line.strip())
    return data

def turn_right(bearing: int) -> int:
    """Retrieve direction after turning right.
    
    Parameters
    ----------
    curr_direction : int
        Current direction ID.
    
    Returns
    -------
    int
        Direction ID after turning right.
    
    """
    if bearing == NORTH:
        return EAST
    if bearing == EAST:
        return SOUTH
    if bearing == SOUTH:
        return WEST
    if bearing == WEST:
        return NORTH
    
def move(
    pos: Tuple[int, int],
    bearing: int,
    blocked: List[Tuple[int, int]]
) -> Tuple[Tuple[int, int], int]:
    """Retrieve position after moving once.
    
    Parameters
    ----------
    pos : Tuple[int, int]
        Current position.
    direction : int
        Current direction
    blocked : List[Tuple[int, int]]
        List of positions that cannot be occupied.

    Returns
    -------
    Tuple[int, int]
        New position after moving once.
    int
        Direction ID after moving once.

    """
    move_valid = False
    while not move_valid:
        move_valid = True
        step = DIR_MAP[bearing]
        # print(step)
        new_pos = (pos[0] + step[0], pos[1] + step[1])
        # print(new_pos)
        if new_pos in blocked:
            move_valid = False
            bearing = turn_right(bearing)

    return new_pos, bearing

def parse_map(room_map: List[str]) -> Tuple[Tuple[int, int], int, List[Tuple[int, int]]]:
    """Parse room map.
    
    Parameters
    ----------
    room_map : List[str]
        Unprocessed room map.
    
    Returns
    -------
    Tuple[int, int]
        Starting position.
    int
        Starting direction ID.
    List[Tuple[int, int]]
        List of positions in that cannot be occupied.
    
    """
    pos = None
    bearing = None
    blocked = []
    for row, vals in enumerate(room_map):
        for col, val in enumerate(vals):
            if val == EMPTY_SPACE:
                continue
            if val == BLOCKED_SPACE:
                blocked.append((row, col))
            elif val == START_UP:
                pos = (row, col)
                bearing = NORTH
            elif val == START_LEFT:
                pos = (row, col)
                bearing = WEST
            elif val == START_RIGHT:
                pos = (row, col)
                bearing = EAST
            else:
                # START_DOWN is a non-standard character, treat it as default
                pos = (row, col)
                bearing = SOUTH
    return pos, bearing, blocked

def in_bounds(pos: Tuple[int, int], ylims: Tuple[int, int], xlims: Tuple[int, int]) -> bool:
    """Check if current position is in bounds.
    
    Parameters
    ----------
    pos : Tuple[int, int]
        Current position.
    ylims : Tuple[int, int]
        Minimum/maximum Y-values.
    xlims : Tuple[int, int]
        Minimum/maximum X-values.
    
    Returns
    -------
    bool
        `True` if position is in bounds.
        `False` if position is out of bounds.

    """
    if ylims[0] <= pos[0] < ylims[1] and xlims[0] <= pos[1] < xlims[1]:
        return True
    return False

def count_distinct_positions(room_map: List[str]) -> int:
    """Count the number of distinct positions visited.
    
    Parameters
    ----------
    room_map : List[str]
        Unprocessed room map.

    Returns
    -------
    int
        The number of distinct positions visited.
    
    """
    occupied = set()
    ylims = (0, len(room_map))
    xlims = (0, len(room_map[0]))
    pos, bearing, blocked = parse_map(room_map)
    while in_bounds(pos, ylims, xlims):
        occupied.add(pos)
        pos, bearing = move(pos, bearing, blocked)
    return len(occupied)

def count_distinct_loop_opportunities(room_map: List[str]) -> int:
    """Count the number of distinct positions where loops can be forced.
    
    Parameters
    ----------
    room_map : List[str]
        Unprocessed room map.

    Returns
    -------
    int
        The number of distinct positions where loops
        can be forced.
    
    """
    loopable = set()
    ylims = (0, len(room_map))
    xlims = (0, len(room_map[0]))
    pos, bearing, blocked = parse_map(room_map)
    path = []
    while in_bounds(pos, ylims, xlims):
        path.append(pos)
        pos, bearing = move(pos, bearing, blocked)
    cntr = Counter(path)
    num_crosses = 0
    for pos, count in cntr.most_common():
        if count < 2:
            break
        idx = path.index(pos) + 1
        first_bearing = (path[idx][0] - pos[0], path[idx][1] - pos[1])
        idx = path.index(pos, idx) + 1
        second_bearing = (path[idx][0] - pos[0], path[idx][1] - pos[1])
        if turn_right(DIR_MAP.index(second_bearing)) == DIR_MAP.index(first_bearing):
            loop_pos = (pos[0] + second_bearing[0], pos[1] + second_bearing[1])
            if in_bounds(loop_pos, ylims, xlims):
                loopable.add(loop_pos)
    print(loopable)
    return len(loopable)

def main() -> None:
    """Script main function."""
    room_map = read_input(INPUT_PATH)
    print("Part I")
    print("-------")
    outp = count_distinct_positions(room_map)
    print(f"Result: {outp}")
    print("======================")
    outp = count_distinct_loop_opportunities(room_map)
    print(outp)
    # print("Part II")
    # print("-------")
    # outp = ???
    # print(f"Result: {outp}")

if __name__ == "__main__":
    main()
