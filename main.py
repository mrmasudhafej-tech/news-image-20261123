#!/usr/bin/env python3
"""Write the 23 November 2026 front page to the output directory.

The finished image is held in this repository as ``entry.png`` (drawn
for this competition day, with that day's news). This program only
copies those exact bytes to ``/output/entry.png`` (or to the directory
named by ``MAKEFUN_OUTPUT_DIR``), so the two grader runs always write
identical bytes. Standard library only; no network access.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_BYTES = 1048576
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def output_dir() -> Path:
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if chosen:
        return Path(chosen)
    return Path("/output")


def read_and_check(source: Path) -> bytes:
    data = source.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over the 1 MiB limit")
    if not data.startswith(PNG_SIGNATURE):
        raise ValueError("entry.png is not a PNG file")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            f"expected {EXPECTED_WIDTH}x{EXPECTED_HEIGHT}, got {width}x{height}"
        )
    return data


def main() -> int:
    repo_dir = Path(__file__).resolve().parent
    source = repo_dir / SOURCE_NAME
    data = read_and_check(source)
    target_dir = output_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / OUTPUT_NAME
    target.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f"wrote {target} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
