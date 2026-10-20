"""Base class shared by all handlers."""
from __future__ import annotations

from ..core.memory import ProcessMemory
from ..core.offsets import OffsetTable


class BaseHandler:
    name = "base"

    def __init__(self, mem: ProcessMemory, offsets: OffsetTable) -> None:
        self.mem = mem
        self.offsets = offsets
        self.enabled = False

    def enable(self) -> None:
        self.enabled = True

    def disable(self) -> None:
        self.enabled = False

    def tick(self) -> None:
        if not self.enabled:
            return
        self._apply()

    def _apply(self) -> None:
        raise NotImplementedError