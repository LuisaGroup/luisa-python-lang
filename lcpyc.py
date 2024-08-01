import argparse
import sys
from typing import List

description = """LuisaCompute Python DSL Compiler
Example:
    python -m lcpyc my_kernel.py --emit cpp -o my_kernel.h
"""


def _main(args: List[str]):
    parser = argparse.ArgumentParser(prog="lcpyc", description=description)
    parser.add_argument("filename")
    parser.add_argument(
        "--emit",
        help="""emit type:
    ir:         Serialized IR in json (Default)
    h|hpp:      C/C++ Header with struct definitions
    rust:       Rust file with struct definitions
    cpp:        Generated C++ source for static compilation
    """,
        choices=["ir", "h", "hpp", "rust"],
    )
    parser.add_argument("-o", "--output", help="output file")
    result = parser.parse_args(args)
    # TODO: Implement the compiler
    raise NotImplementedError(result)


if __name__ == "__main__":
    _main(sys.argv[1:])
