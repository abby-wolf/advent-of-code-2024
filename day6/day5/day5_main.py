from typing import List, Dict, Set, Tuple

INPUT_PATH = "inp.txt"
RULE_DELIM = "|"
INSTR_DELIM = ","

def read_data(inp_path: str) -> Tuple[List[str], List[str], List[List[str]]]:
    """Read input data.
    
    Parameters
    ----------
    inp_path : str
        Input data filepath.

    Returns
    -------
    List[str]
        Page ordering rules column X data.
    List[str]
        Page ordering rules column Y data.
    List[List[str]]
        Page update instructions.
    
    """
    xcol = []
    ycol = []
    instr = []
    with open(inp_path, "r", encoding="utf-8") as input_file:
        for line in input_file.readlines():
            line = line.strip()
            if not line:
                continue
            if RULE_DELIM in line:
                tmp = line.split(RULE_DELIM)
                xcol.append(tmp[0])
                ycol.append(tmp[1])
                continue
            instr.append(line.split(INSTR_DELIM))
    return xcol, ycol, instr

def create_rules_lut(xdata: List[str], ydata: List[str]) -> Dict[str, Set[str]]:
    """Create ordering rules lookup table.
    
    Parameters
    ----------
    xdata : List[str]
        Page ordering rules column X data.
    ydata : List[str]
        Page ordering rules column Y data.

    Returns
    -------
    Dict[str, Set[str]]
        Dictionary containing pages mapped to a
        set of all pages that must preceed them.
    
    """
    lut: Dict[str, Set[str]] = {}
    for key, val in zip(ydata, xdata):
        if not key in lut:
            lut[key] = set()
        lut[key].add(val)

    return lut

def update_is_ok(upd: List[str], lut: Dict[str, Set[str]]) -> bool:
    """Determine if a page update is valid.
    
    Parameters
    ----------
    upd : List[str]
        The page update to validate.
    lut : Dict[str, Set[str]]
        Page ordering rules lookup table.
    
    Returns
    -------
    bool
        `True` if page update is valid.
        `False` if page update is invalid.

    """
    idx = 0
    for page in upd:
        idx += 1
        if page not in lut:
            continue
        upd_set = set(upd[idx:])
        if upd_set & lut[page]:
            return False

    return True

def fix_update(upd: List[str], lut: Dict[str, Set[str]]) -> List[str]:
    """Fix an invalid page update.
    
    Parameters
    ----------
    upd : List[str]
        The invalid update to fix.
    lut : Dict[str, Set[str]]
        Page ordering rules lookup table.

    Returns
    -------
    List[str]
        The fixed page update.
    
    """
    idx = 0
    fixed = upd.copy()
    while idx < len(fixed):
        page = fixed[idx]
        if page not in lut:
            idx += 1
            continue
        comp = set(fixed[idx+1:])
        to_move = comp & lut[page]
        if to_move:
            for inc, val in enumerate(to_move):
                fixed.insert(idx+inc, fixed.pop(fixed.index(val)))
            continue
        idx += 1
    return fixed
            

def analyze_page_updates(page_upds: List[List[str]], rules_lut: Dict[str, Set[str]]) -> int:
    """Analyze the proposed page updates.
    
    Function determines the validity of the proposed
    pages updates and sums the middle page number of
    all valid updates.

    Parameters
    ----------
    page_upds : List[List[str]]
        The proposed page updates.
    rules_lut : Dict[str, Set[str]]
        Page ordering rules lookup table.
    
    Returns
    -------
    int
        The sum of the middle page number of all
        valid updates.

    """
    total = 0
    for upd in page_upds:
        if update_is_ok(upd, rules_lut):
            total += int(upd[(len(upd) - 1)//2])
    return total

def analyze_fixed_page_updates(page_upds: List[List[str]], rules_lut: Dict[str, Set[str]]) -> int:
    """Analyzed the fixed proposed page updates.
    
    Function fixes any proposed page updates which
    register as invalid and sums the middle page
    number of all such page updates after fixes
    are applied.

    Parameters
    ----------
    page_upds : List[List[str]]
        The proposed page updates.
    rules_lut : Dict[str, Set[str]]
        Page ordering rules lookup table.
    
    Returns
    -------
    int
        The sum of the middle page number of all
        fixed updates.
    
    """
    total = 0
    for upd in page_upds:
        if update_is_ok(upd, rules_lut):
            continue
        new_upd = fix_update(upd, rules_lut)
        total += int(new_upd[(len(new_upd) - 1)//2])
    return total


def main() -> None:
    """Script main function."""
    data_xcol, data_ycol, page_upds = read_data(INPUT_PATH)
    rules_lut = create_rules_lut(data_xcol, data_ycol)
    print("Part I")
    print("-------")
    outp = analyze_page_updates(page_upds, rules_lut)
    print(f"Result: {outp}")
    print("======================")
    print("Part II")
    print("-------")
    outp = analyze_fixed_page_updates(page_upds, rules_lut)
    print(f"Result: {outp}")

if __name__ == "__main__":
    main()
