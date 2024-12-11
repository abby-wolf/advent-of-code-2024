from collections import Counter
import re
from typing import List, Tuple

INPUT_PATH = "inp.txt"

def read_data(inp_path: str) -> Tuple[List[int], List[int]]:
    """Parse the input data.
    
    Parameters
    ----------
    path : str
        Input data filepath.

    Returns
    -------
    List[int]
        Data from the first column.
    List[int]
        Data from the second column.
    
    """
    with open(inp_path, "r", encoding="utf-8") as input_file:
        col0_data = []
        col1_data = []
        for line in input_file.readlines():
            if line:
                matches = re.findall(r"\d+", line)
                col0_data.append(int(matches[0]))
                col1_data.append(int(matches[1]))
        return col0_data, col1_data

def get_distance_sum(col0: List[int], col1: List[int]) -> int:
    """Calculate the distance sum of the data.
    
    Calculates the sum of the distances between
    sorted data points. Sort is performed during
    function operation, thus parameter lists do
    not need to be sorted beforehand.

    Parameters
    ----------
    col0 : List[int]
        Data from the first column.
    col1 : List[int]
        Data from the second column.
    
    Returns
    -------
    int
        The sum of the sorted data point distances.
    
    """
    total = 0
    for val0, val1 in zip(sorted(col0), sorted(col1)):
        total += abs(val0 - val1)
    return total

def get_similarity_score(col0: List[int], col1: List[int]) -> int:
    """Calculate the similarity score of the data.
    
    Calculates similarity score between the two
    columns based on the number of times any value
    in column 0 appears in column 1.

    Parameters
    ----------
    col0 : List[int]
        Data from the first column.
    col1 : List[int]
        Data from the second column.
    
    Returns
    -------
    int
        The similarity score of the data.
    
    """
    cnt0 = Counter(col0)
    cnt1 = Counter(col1)
    total = 0
    for val in cnt0.keys():
        if val in cnt1:
            total += cnt0[val]*val*cnt1[val]
    return total


def main() -> None:
    """Script main function."""
    col0_data, col1_data = read_data(INPUT_PATH)
    print("Part I")
    print("-------")
    outp = get_distance_sum(col0_data, col1_data)
    print(f"Result: {outp}")
    print("=============================")
    print("Part II")
    print("-------")
    outp = get_similarity_score(col0_data, col1_data)
    print(f"Result: {outp}")

if __name__ == "__main__":
    main()
