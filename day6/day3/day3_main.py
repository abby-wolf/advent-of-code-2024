import re
from typing import Generator, List

INPUT_PATH = "inp.txt"

def read_data(inp_path: str) -> str:
    """Read input data.

    Parameters
    ----------
    inp_path : str
        Input filepath.

    Returns
    -------
    str
        The data read from the input file.
    
    """
    with open(inp_path, "r", encoding="utf-8") as input_file:
        input_data = input_file.read()
    return input_data

def parse_data(pattern_str: str, inp_data: str) -> Generator[re.Match, None, None]:
    """Parse input data.
    
    Extracts the multiplication operations from
    the input data based on the given pattern.

    Parameters
    ----------
    pattern_str : str
        RegEx pattern to use for the extraction.
    inp_data : str
        Data to parse.

    Returns
    -------
    Generator[Tuple[int, int], None, None]
        Generator object which yields the values
        to multiply for each multiplication operator.
    
    """
    pattern = re.compile(pattern_str)
    for valid in re.finditer(pattern, inp_data):
        yield valid

def get_ignore_indices(inp_data: str) -> List[int]:
    """Extract the text indices that should be ignored.
    
    Parameters
    ----------
    inp_data : str
        Data to extract indices from
    
    Returns
    -------
    List[int]
        List of string indices to ignore.

    """
    pattern_str = r"do(n\'t)?\(\)"
    start = None
    # stop = None
    enabled = True
    ignore = []
    for valid in parse_data(pattern_str, inp_data):
        if valid.group(1) is not None:
            if enabled:
                start = valid.end()
                enabled = False
        else:
            if not enabled:
                ignore.extend([*range(start, valid.start())])
                enabled = True
    if not enabled:
        ignore.extend([*range(start, len(inp_data))])
    return ignore


def sum_mul_operations(inp_data: str, conditional: bool = False) -> int:
    """Calculate the sum of all valid mul operations.
    
    Parameters
    ----------
    inp_data : str
        Input data to use for calculation.
    conditional : bool
        If `True`, evaluate mul operations conditionally.

    Returns
    -------
    int
        The sum of all valid mul operations.

    """
    total = 0
    ignore_idx = []
    if conditional:
        ignore_idx = get_ignore_indices(inp_data)
    pattern_str = r"mul\((\d{1,3}),(\d{1,3})\)"
    for valid in parse_data(pattern_str, inp_data):
        if valid.start() in ignore_idx:
            continue
        # print(valid.start())
        total += int(valid.group(1))*int(valid.group(2))
    return total

def main() -> None:
    """Script main function."""
    inp_data = read_data(INPUT_PATH)
    print("Part I")
    print("-------")
    outp = sum_mul_operations(inp_data)
    print(f"Result: {outp}")
    print("======================")
    print("Part II")
    print("-------")
    outp = sum_mul_operations(inp_data, conditional=True)
    print(f"Result: {outp}")

if __name__ == "__main__":
    main()
