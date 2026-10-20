"""Set or freeze genetics stats (STR/DEX/INT/CON) on the active cat."""
from __future__ import annotations

from .base import BaseHandler


class StatHandler(BaseHandler):
    name = "stats"

    def __init__(self, *args, target: int = 99, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.target = target

    def _resolve(self) -> int:
        assert self.mem.base is not None
        chain = self.offsets.stats["chain"]
        return self.mem.resolve_chain(self.mem.base + chain[0], chain[1:])

    def _apply(self) -> None:
        try:
            base = self._resolve()
            for key in ("str", "dex", "int", "con"):
                off = self.offsets.stats[key]
                if self.mem.read_int(base + off) < self.target:
                    self.mem.write_int(base + off, self.target)
        except Exception:
            pass

    def snapshot(self) -> dict:
        try:
            base = self._resolve()
            return {k: self.mem.read_int(base + self.offsets.stats[k]) for k in ("str", "dex", "int", "con")}
        except Exception:
            return {"str": 0, "dex": 0, "int": 0, "con": 0}