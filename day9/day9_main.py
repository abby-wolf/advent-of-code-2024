from typing import List

INPUT_PATH = "inp.txt"

def read_input(inp_path: str) -> str:
    with open(inp_path, "r", encoding="utf-8") as input_file:
        data = input_file.read()
    return data.strip()

def parse_input(mem_map: str) -> List[int]:
    mem_blocks = []
    map_num = 0
    for val in mem_map[::2]:
        mem_blocks.extend([map_num]*int(val))
        map_num += 1
    return mem_blocks

def calc_checksum(mem_map: str) -> int:
    mem_blocks = parse_input(mem_map)
    checksum = 0
    blk_ptr = 0
    global_idx = 0
    for val in mem_map:
        for _ in range(int(val)):
            checksum += global_idx*mem_blocks.pop(blk_ptr)
            if not mem_blocks:
                return checksum
            global_idx += 1
        blk_ptr = (blk_ptr + 1)%-2
    return checksum

def calc_checksum_byfile(mem_map: str) -> int:
    mem_blocks = parse_input(mem_map)
    file_blks = mem_map[::-2]
    free_blks = mem_map[1::2]

def main() -> None:
    """Script main function."""
    mem_map = read_input(INPUT_PATH)
    print("Part I")
    print("-------")
    outp = calc_checksum(mem_map)
    print(f"Result: {outp}")
    print("======================")
    # print("Part II")
    # print("-------")
    # outp = count_unique_total_antinodes(data)
    # print(f"Result: {outp}")

if __name__ == "__main__":
    main()
