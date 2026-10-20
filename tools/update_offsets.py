"""Utility to refresh offsets/current.toml from a running process dump.

Usage:
    python -m tools.update_offsets --process Mewgenics.exe --out offsets/current.toml
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import tomli_w

from mewgenics_trainer.core.memory import ProcessMemory
from mewgenics_trainer.core.offsets import OffsetTable


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--process", default="Mewgenics.exe")
    p.add_argument("--out", default="offsets/current.toml")
    args = p.parse_args(argv)

    mem = ProcessMemory(args.process)
    if not mem.attach():
        print(f"could not attach to {args.process}", file=sys.stderr)
        return 1
    try:
        table = OffsetTable.load()
        data = {"gold": table.gold, "stats": table.stats, "cats": table.cats}
        Path(args.out).write_bytes(tomli_w.dumps(data).encode())
        print(f"wrote {args.out}")
    finally:
        mem.detach()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())