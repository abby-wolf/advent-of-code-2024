import re
from typing import List, Generator

INPUT_PATH = "inp.txt"

def read_reports(inp_path: str) -> Generator[List[int], None, None]:
    """Parse input data.
    
    Yields each line of input data.

    Parameters
    ----------
    path : str
        Input filepath.

    Returns
    -------
    Generator[List[int], None, None]
        Generator object which yields preprocessed
        input data line-by-line.
    
    """
    with open(inp_path, "r", encoding="utf-8") as input_file:
        for line in input_file.readlines():
            if not line:
                continue
            data = re.findall("\d+", line)
            yield [int(x) for x in data]

def is_safe(report: List[int]) -> bool:
    """Determine if a report is safe.
    
    Parameters
    ----------
    report : List[int]
        The report to evaluate.

    Returns
    -------
    bool
        `True` if the report is safe.
        `False` if the report is not safe.
    
    """
    diffs = [x - y for x, y in zip(report[:-1], report[1:])]
    if 0 in diffs:
        return False
    if abs(sum([x/abs(x) for x in diffs])) != len(diffs):
        return False
    if max(diffs) > 3 or min(diffs) < -3:
        return False
    return True
    
def is_safe_dampened(report: List[int]) -> bool:
    """Determine if a report is safe after dampening.
    
    Parameters
    ----------
    report : List[int]
        The report to evaluate.

    Returns
    -------
    bool
        `True` if the report is safe.
        `False` if the report is not safe.
    
    """
    if is_safe(report):
        return True
    for idx in range(len(report)):
        if is_safe(report[:idx] + report[idx+1:]):
            return True
    return False

def get_num_safe_reports(dampened: bool = False) -> int:
    """Get the number of safe reports.
    
    Returns
    -------
    int
        The number of safe reports.
    
    """
    total = 0
    for report in read_reports(INPUT_PATH):
        if dampened and is_safe_dampened(report):
            total += 1
        elif is_safe(report):
            total += 1
    return total

def main() -> None:
    """Script main function."""
    print("Part I")
    print("-------")
    outp = get_num_safe_reports()
    print(f"Result: {outp}")
    print("======================")
    print("Part II")
    print("-------")
    outp = get_num_safe_reports(dampened=True)
    print(f"Result: {outp}")

if __name__ == "__main__":
    main()
