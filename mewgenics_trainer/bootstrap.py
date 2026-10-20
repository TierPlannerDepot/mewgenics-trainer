"""Session bootstrap — ties memory, handlers, and feature modules together."""
from __future__ import annotations

from typing import Optional

from .core.memory import ProcessMemory
from .core.offsets import OffsetTable
from .config.settings import TrainerSettings
from .handlers.gold_handler import GoldHandler
from .handlers.stat_handler import StatHandler
from .handlers.cat_handler import CatHandler
from .services.overlay_service import OverlayService
from .utils.logger import get_logger

log = get_logger("bootstrap")


class TrainerSession:
    def __init__(self, process_name: str, settings: TrainerSettings) -> None:
        self.process_name = process_name
        self.settings = settings
        self._mem: Optional[ProcessMemory] = None
        self._offsets = OffsetTable.load()
        self._handlers: list = []
        self._overlay: Optional[OverlayService] = None
        self.running = False

    @property
    def pid(self) -> Optional[int]:
        return self._mem.pid if self._mem else None

    @property
    def base(self) -> Optional[int]:
        return self._mem.base if self._mem else None

    def attach(self) -> bool:
        self._mem = ProcessMemory(self.process_name)
        if not self._mem.attach():
            self._mem = None
            return False
        self._handlers = [
            GoldHandler(self._mem, self._offsets),
            StatHandler(self._mem, self._offsets),
            CatHandler(self._mem, self._offsets),
        ]
        if not self.settings.disable_overlay:
            self._overlay = OverlayService(self._handlers)
        return True

    def enable_all(self) -> None:
        for h in self._handlers:
            h.enable()
        self.running = True

    def tick(self) -> None:
        for h in self._handlers:
            h.tick()
        if self._overlay:
            self._overlay.render()

    def detach(self) -> None:
        self.running = False
        for h in self._handlers:
            h.disable()
        if self._overlay:
            self._overlay.close()
        if self._mem:
            self._mem.detach()
        log.info("detached")