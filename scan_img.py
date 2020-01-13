#!/usr/bin/python3
import argparse
import os
import math


def batch(iterable, size, all_inclusive=False):
    s = size if not all_inclusive else 1
    for i in range(0, len(iterable), s):
        yield iterable[i:i + size]


def scan_for_bytes(bytepattern: bytes, filepath: str, find_all: bool = False):
    """Opens a file and scans for specific byte pattern
    """
    offsets = list()
    with open(filepath, "rb") as f:
        for i, b in enumerate(batch(f.read(), len(bytepattern), True)):
            if bytepattern == b:
                offsets.append(i)
                if find_all is False:
                    break
    return offsets


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("pattern", help="bytepattern in hex")
    parser.add_argument("path", help="Path to file to scan", type=str)
    parser.add_argument("-a", "--all-instances",
                        help="find all instances of pattern",
                        action="store_true", default=False)
    parser.add_argument("-s", "--string", help="Interpret pattern as a string",
                        action="store_true", default=False)
    args = parser.parse_args()
    if os.path.isfile(args.path) is False:
        print(f"path must be a path to a file")
        quit(1)

    # Convert the input to bytes
    if args.string is True:
        byte_pattern = args.pattern.encode()
    else:
        i_val = int(args.pattern, 16)
        byte_pattern = int.to_bytes(i_val, math.ceil(i_val.bit_length() / 8), 'big')

    offsets = scan_for_bytes(byte_pattern, args.path, args.all_instances)
    if len(offsets) == 0:
        print(f"{args.pattern} not found")
    else:
        print(f"{args.pattern} found at the following offsets")
        for i in offsets:
            print(hex(i))

