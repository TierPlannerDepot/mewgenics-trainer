"""Freeze or set the player's gold amount."""
from __future__ import annotations

from .base import BaseHandler


class GoldHandler(BaseHandler):
    name = "gold"

    def __init__(self, *args, target: int = 999_999, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.target = target

    def _resolve(self) -> int:
        assert self.mem.base is not None
        chain = self.offsets.gold["chain"]
        return self.mem.resolve_chain(self.mem.base + chain[0], chain[1:])

    def _apply(self) -> None:
        try:
            addr = self._resolve()
            current = self.mem.read_int(addr)
            if current < self.target:
                self.mem.write_int(addr, self.target)
        except Exception:
            pass

    def current_gold(self) -> int:
        try:
            return self.mem.read_int(self._resolve())
        except Exception:
            return 0