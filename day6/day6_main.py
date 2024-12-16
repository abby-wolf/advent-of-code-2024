from bisect import bisect_left, insort_left
from typing import List, Tuple, Dict
import time

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

class PositionMap:
    def __init__(self, blocked: List[Tuple[int]]) -> None:
        col_map, row_map = self._get_maps(blocked)
        self.col_map: Dict[int, List[int]] = col_map
        self.row_map: Dict[int, List[int]] = row_map

    def jump_to_point(self, pos: Tuple[int, int], bearing: int) -> int:
        new_pos = None
        if bearing == NORTH:
            potential_blks = self.col_map.get(pos[1])
            if potential_blks is not None and min(potential_blks) < pos[0]:
                new_pos = potential_blks[bisect_left(potential_blks, pos[0]) - 1] + 1
            return new_pos
        if bearing == EAST:
            potential_blks = self.row_map.get(pos[0])
            if potential_blks is not None and max(potential_blks) > pos[1]:
                new_pos = potential_blks[bisect_left(potential_blks, pos[1])] - 1
            return new_pos
        if bearing == SOUTH:
            potential_blks = self.col_map.get(pos[1])
            if potential_blks is not None and max(potential_blks) > pos[0]:
                new_pos = potential_blks[bisect_left(potential_blks, pos[0])] - 1
            return new_pos
        if bearing == WEST:
            potential_blks = self.row_map.get(pos[0])
            if potential_blks is not None and min(potential_blks) < pos[1]:
                new_pos = potential_blks[bisect_left(potential_blks, pos[1]) - 1] + 1
            return new_pos
        raise ValueError("Invalid bearing!!")

    def jump_to_coord(self, pos: Tuple[int, int], bearing: int) -> Tuple[int, int]:
        new_pos = None
        if bearing == NORTH:
            potential_blks = self.col_map.get(pos[1])
            if potential_blks is not None and min(potential_blks) < pos[0]:
                new_pos = (potential_blks[bisect_left(potential_blks, pos[0]) - 1] + 1, pos[1])
            return new_pos
        if bearing == EAST:
            potential_blks = self.row_map.get(pos[0])
            if potential_blks is not None and max(potential_blks) > pos[1]:
                new_pos = (pos[0], potential_blks[bisect_left(potential_blks, pos[1])] - 1)
            return new_pos
        if bearing == SOUTH:
            potential_blks = self.col_map.get(pos[1])
            if potential_blks is not None and max(potential_blks) > pos[0]:
                new_pos = (potential_blks[bisect_left(potential_blks, pos[0])] - 1, pos[1])
            return new_pos
        if bearing == WEST:
            potential_blks = self.row_map.get(pos[0])
            if potential_blks is not None and min(potential_blks) < pos[1]:
                new_pos = (pos[0], potential_blks[bisect_left(potential_blks, pos[1]) - 1] + 1)
            return new_pos
        raise ValueError("Invalid bearing!!")

    def add_block(self, row: int, col: int) -> None:
        if row not in self.row_map:
            self.row_map[row] = [col]
        else:
            insort_left(self.row_map[row], col)
        if col not in self.col_map:
            self.col_map[col] = [row]
        else:
            insort_left(self.col_map[col], row)

    def remove_block(self, row: int, col: int) -> None:
        rval = self.row_map.get(row)
        cval = self.col_map.get(col)
        if rval is not None:
            if len(rval) == 1:
                self.row_map.pop(row)
            else:
                self.row_map[row].pop(bisect_left(rval, col))
        if cval is not None:
            if len(cval) == 1:
                self.col_map.pop(col)
            else:
                self.col_map[col].pop(bisect_left(cval, row))
                #sdfgsd

    def _get_maps(
        self,
        pos: List[Tuple[int]]
    ) -> Tuple[Dict[int, List[int]], Dict[int, List[int]]]:
        col_map: Dict[int, List[int]] = {}
        row_map: Dict[int, List[int]] = {}
        for row, col in pos:
            if col not in col_map:
                col_map[col] = []
            if row not in row_map:
                row_map[row] = []
            col_map[col].append(row)
            row_map[row].append(col)
        return col_map, row_map
            

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

def creates_loop(
    start_pos: Tuple[int, int],
    pmap: PositionMap,
    blk: Tuple[int, int],
    bearing: int
) -> bool:
    pmap.add_block(blk[0], blk[1])
    slow_ptr = pmap.jump_to_coord(start_pos, bearing)
    if slow_ptr is None:
        pmap.remove_block(blk[0], blk[1])
        return False
    slow_ptr_bearing = (bearing + 1)%4
    fast_ptr = pmap.jump_to_coord(slow_ptr, slow_ptr_bearing)
    if fast_ptr is None:
        pmap.remove_block(blk[0], blk[1])
        return False
    fast_ptr_bearing = (slow_ptr_bearing + 1)%4

    is_loop = False
    while True:
        slow_ptr = pmap.jump_to_coord(slow_ptr, slow_ptr_bearing)
        slow_ptr_bearing = (slow_ptr_bearing + 1)%4

        fast_ptr = pmap.jump_to_coord(fast_ptr, fast_ptr_bearing)
        if fast_ptr is None:
            break
        fast_ptr_bearing = (fast_ptr_bearing + 1)%4
        fast_ptr = pmap.jump_to_coord(fast_ptr, fast_ptr_bearing)
        if fast_ptr is None:
            break
        fast_ptr_bearing = (fast_ptr_bearing + 1)%4
        if fast_ptr == slow_ptr and fast_ptr_bearing == slow_ptr_bearing:
            is_loop = True
            break
    pmap.remove_block(blk[0], blk[1])
    return is_loop

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
    oob_ind = [0, len(room_map[0]) - 1, len(room_map) - 1, 0]
    shift_mods = [-1, 1, 1, -1]
    shift_idx = [0, 1, 0, 1]
    pos, bearing, blocked = parse_map(room_map)
    pmap = PositionMap(blocked)
    occupied.add(pos)
    in_bounds = True
    while in_bounds:
        new_pos = pmap.jump_to_point(pos, bearing)
        if new_pos is None:
            in_bounds = False
            new_pos = oob_ind[bearing]
        nsteps = abs(pos[shift_idx[bearing]] - new_pos)
        sft_mod = shift_mods[bearing]

        for sft in range(nsteps):
            if bearing in [NORTH, SOUTH]:
                occupied.add((pos[0] + sft_mod*(sft + 1), pos[1]))
            else:
                occupied.add((pos[0], pos[1] + sft_mod*(sft + 1)))
        pos = (new_pos, pos[1]) if bearing in [NORTH, SOUTH] else (pos[0], new_pos)
        bearing = (bearing + 1)%4
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
    loopable = 0
    occupied = set()
    oob_ind = [0, len(room_map[0]) - 1, len(room_map) - 1, 0]
    shift_mods = [-1, 1, 1, -1]
    shift_idx = [0, 1, 0, 1]
    pos, bearing, blocked = parse_map(room_map)
    pmap = PositionMap(blocked)
    occupied.add(pos)
    in_bounds = True
    while in_bounds:
        new_pos = pmap.jump_to_point(pos, bearing)
        if new_pos is None:
            in_bounds = False
            new_pos = oob_ind[bearing]
        nsteps = abs(pos[shift_idx[bearing]] - new_pos)
        sft_mod = shift_mods[bearing]
        tmp_bearing = (bearing + 1)%4
        for _ in range(nsteps):
            if bearing in [NORTH, SOUTH]:
                tmp_pos = (pos[0] + sft_mod, pos[1])
            else:
                tmp_pos = (pos[0], pos[1] + sft_mod)
            if tmp_pos in occupied:
                pos = tmp_pos
                continue
            occupied.add(tmp_pos)
            if creates_loop(pos, pmap, tmp_pos, tmp_bearing):
                loopable += 1
            pos = tmp_pos
        bearing = tmp_bearing
    return loopable
                

def main() -> None:
    """Script main function."""
    room_map = read_input(INPUT_PATH)
    print("Part I")
    print("-------")
    outp = count_distinct_positions(room_map)
    print(f"Result: {outp}")
    print("======================")
    print("Part II")
    print("-------")
    outp = count_distinct_loop_opportunities(room_map)
    print(f"Result: {outp}")

if __name__ == "__main__":
    main()
