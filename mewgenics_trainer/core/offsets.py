"""Offset table loaded from offsets/current.toml with fallback defaults."""
from __future__ import annotations

import tomli
from dataclasses import dataclass
from pathlib import Path

_OFFSETS_FILE = Path(__file__).resolve().parent.parent.parent / "offsets" / "current.toml"

_DEFAULTS = {
    "gold": {"chain": [0x02A1F8C0, 0x18, 0x0], "value": 0x0},
    "stats": {"chain": [0x02A1F9A0, 0x10, 0x48], "str": 0x0, "dex": 0x4, "int": 0x8, "con": 0xC},
    "cats": {"chain": [0x02A1FB10, 0x0, 0x20], "count": 0x0, "first": 0x8, "stride": 0x120},
}


@dataclass(frozen=True)
class OffsetTable:
    gold: dict
    stats: dict
    cats: dict

    @classmethod
    def load(cls, path: Path | None = None) -> "OffsetTable":
        target = path or _OFFSETS_FILE
        data = _DEFAULTS
        if target.exists():
            with target.open("rb") as fh:
                data = tomli.load(fh)
        return cls(gold=data["gold"], stats=data["stats"], cats=data["cats"])