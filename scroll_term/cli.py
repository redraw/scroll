#!/usr/bin/env python3
import os
import time
import sys
import argparse
import textwrap
from collections import deque
from typing import TextIO


def scroll(file: TextIO, delay: float = 0, max_lines: int = 10):
    term_size = os.get_terminal_size()
    max_lines = max_lines or term_size.lines

    buffer = deque(["\n"] * max_lines, maxlen=max_lines)

    for line in file:
        buffer.append(textwrap.shorten(str(line), width=term_size.columns - 1) + "\n")
        for item in buffer:
            sys.stdout.write(f"{item}\033[K")
        sys.stdout.write(f"\033[{max_lines}A\033[K")
        if delay > 0:
            time.sleep(delay)


def main():
    parser = argparse.ArgumentParser(description="Scroll through stdout!")
    parser.add_argument("-d", "--delay", type=int, default=0, help="delay in seconds between lines (default 0)")
    parser.add_argument("-l", "--lines", type=int, default=10, help="max lines, set to 0 for full screen (default 10)")
    parser.add_argument(
        "file",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="file, defaults to stdin",
    )
    args = parser.parse_args()

    try:
        scroll(
            file=args.file,
            delay=args.delay,
            max_lines=args.lines,
        )
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
