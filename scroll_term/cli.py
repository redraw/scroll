#!/usr/bin/env python3
import os
import time
import sys
import argparse
import textwrap
from collections import deque
from typing import TextIO


def print_buffer(buffer: deque):
    for item in buffer:
        sys.stdout.write(f"{item}\033[K")


def scroll(file: TextIO, delay: float = 0, max_lines: int = 10, fix_lines: int = 0):
    term_size = os.get_terminal_size()
    total_lines = (max_lines or term_size.lines) - fix_lines

    # print header
    for _ in range(fix_lines):
        line = next(file)
        sys.stdout.write(line)

    buffer = deque(["\n"] * total_lines, maxlen=total_lines)
    # move cursor down
    print_buffer(buffer)

    for line in file:
        buffer.append(next(iter(textwrap.wrap(str(line), width=term_size.columns - 1)), "") + "\n")
        # move cursor up
        sys.stdout.write(f"\033[{total_lines}A\033[K")
        # print buffer
        print_buffer(buffer)
        # add delay
        if delay > 0:
            time.sleep(delay)


def main():
    parser = argparse.ArgumentParser(description="Scroll through stdout!")
    parser.add_argument("-d", "--delay", type=float, default=0, help="delay in seconds between lines (default 0)")
    parser.add_argument("-l", "--lines", type=int, default=10, help="max lines, set to 0 for full screen (default 10)")
    parser.add_argument("-f", "--fix", type=int, default=0, help="fix first x lines while scrolling")
    parser.add_argument( "file", nargs="?", type=argparse.FileType("r"), default=sys.stdin, help="file, defaults to stdin")
    args = parser.parse_args()

    try:
        scroll(
            file=args.file,
            delay=args.delay,
            max_lines=args.lines,
            fix_lines=args.fix,
        )
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
