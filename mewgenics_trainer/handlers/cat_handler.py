"""Enumerate the player's cat roster from the memory-linked list."""
from __future__ import annotations

from dataclasses import dataclass

from .base import BaseHandler


@dataclass
class CatEntry:
    slot: int
    address: int
    name_id: int
    level: int


class CatHandler(BaseHandler):
    name = "cats"

    def _resolve(self) -> int:
        assert self.mem.base is not None
        chain = self.offsets.cats["chain"]
        return self.mem.resolve_chain(self.mem.base + chain[0], chain[1:])

    def _apply(self) -> None:
        # read-only handler — nothing to write per tick
        return

    def enumerate(self, limit: int = 32) -> list[CatEntry]:
        cats = self.offsets.cats
        try:
            head = self._resolve()
            count = min(self.mem.read_int(head + cats["count"]), limit)
            first = self.mem.read_pointer(head + cats["first"])
            out: list[CatEntry] = []
            for i in range(count):
                addr = first + i * cats["stride"]
                out.append(CatEntry(slot=i, address=addr,
                                    name_id=self.mem.read_int(addr),
                                    level=self.mem.read_int(addr + 0x8)))
            return out
        except Exception:
            return []