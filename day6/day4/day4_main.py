from typing import List, Tuple
from itertools import product

INPUT_PATH = "inp.txt"
EMPTY = "."

def read_data(inp_path: str) -> List[List[str]]:
    """Read input data.
    
    Parameters
    ----------
    inp_path : str
        Input data filepath.

    Returns
    -------
    List[List[str]]
        Input parsed into a grid.
    
    """
    data_grid = []
    with open(inp_path, "r", encoding="utf-8") as input_file:
        for line in input_file.readlines():
            if line:
                data_grid.append(EMPTY + line.strip() + EMPTY)
    border_row = EMPTY*len(data_grid[0])
    data_grid.insert(0, border_row)
    data_grid.append(border_row)
    return data_grid

def search_grid_for_pattern(grid: List[str], pattern: str = "XMAS") -> int:
    """Search the grid for the given pattern.
    
    Parameters
    ----------
    grid : List[str]
        The grid to search.
    pattern : str
        The pattern to search for.

    Returns
    -------
    int
        The number of time the pattern appears
        in the grid.
    
    """
    total = 0
    mask = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for row, col in product(range(len(grid)), range(len(grid[0]))):
        if grid[row][col] == EMPTY:
            continue
        if grid[row][col] == pattern[0]:
            for xstep, ystep in mask:
                idx = 1
                pos = (row + ystep, col + xstep)
                match_found = False
                if grid[pos[0]][pos[1]] == EMPTY:
                    continue
                while idx < len(pattern):
                    if grid[pos[0]][pos[1]] == pattern[idx]:
                        idx += 1
                        pos = (pos[0] + ystep, pos[1] + xstep)
                        match_found = idx == len(pattern)
                        continue
                    break
                if match_found:
                    total += 1
    return total

# def check_line(grid: List[str], pattern: str, start_pos: Tuple[int, int], step: Tuple[int, int]) -> bool:
#     """Search the grid for the given pattern.
    
#     Parameters
#     ----------
#     grid : List[str]
#         The grid to search.
#     pattern : str
#         The pattern to check for.
#     start_pos : Tuple[int, int]
#         The position at which the pattern starts.

#     Returns
#     -------
#     bool
#         `True` if the line contains the pattern.
#         in the grid.
    
#     """

def search_grid_for_x_pattern(grid: List[str], pattern: str = "MAS") -> int:
    """Search the grid for the given pattern in X shapes.
    
    Parameters
    ----------
    grid : List[str]
        The grid to search.
    pattern : str
        The pattern to search for.

    Returns
    -------
    int
        The number of time the pattern appears
        in the grid.
    
    """
    if not len(pattern) % 2 == 1:
        raise ValueError("Pattern must have an odd number of characters.")
    total = 0
    leg_length = center_idx = int((len(pattern) - 1)/2)
    valid_term = (pattern[0], pattern[-1])
    for row, col in product(range(len(grid)), range(len(grid[0]))):
        if grid[row][col] == EMPTY:
            continue
        if grid[row][col] == pattern[center_idx]:
            if row - leg_length < 0 or row + leg_length >= len(grid):
                continue
            if col - leg_length < 0 or col + leg_length >= len(grid[0]):
                continue
            term_pos = grid[row - leg_length][col - leg_length]
            term_neg = grid[row - leg_length][col + leg_length]
            if term_pos == EMPTY or term_pos not in valid_term:
                continue
            if term_neg == EMPTY or term_neg not in valid_term:
                continue
            pos_pattern = pattern if term_pos == pattern[0] else pattern[::-1]
            neg_pattern = pattern if term_neg == pattern[0] else pattern[::-1]
            pos_str = ""
            neg_str = ""
            for step in range(leg_length, -(leg_length + 1), -1):
                pos_str += grid[row - step][col - step]
                neg_str += grid[row - step][col + step]
            if pos_str == pos_pattern and neg_str == neg_pattern:
                total += 1
    return total


def main() -> None:
    """Script main function."""
    inp_data = read_data(INPUT_PATH)
    print("Part I")
    print("-------")
    outp = search_grid_for_pattern(inp_data)
    print(f"Result: {outp}")
    print("======================")
    print("Part II")
    print("-------")
    outp = search_grid_for_x_pattern(inp_data)
    print(f"Result: {outp}")

if __name__ == "__main__":
    main()
    