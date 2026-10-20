"""Minimal console overlay that prints live trainer state."""
from __future__ import annotations

import sys
from typing import Iterable

from colorama import Fore, Style, init as colorama_init

colorama_init()


class OverlayService:
    def __init__(self, handlers: Iterable) -> None:
        self.handlers = list(handlers)
        self._open = True

    def render(self) -> None:
        if not self._open:
            return
        parts = []
        for h in self.handlers:
            label = getattr(h, "name", "?")
            if hasattr(h, "current_gold"):
                parts.append(f"{label}={h.current_gold()}")
            elif hasattr(h, "snapshot"):
                snap = h.snapshot()
                parts.append(f"{label}=" + ",".join(f"{k}:{v}" for k, v in snap.items()))
            elif hasattr(h, "enumerate"):
                parts.append(f"{label}={len(h.enumerate())}")
        line = f"[Mewgenics Trainer] " + " | ".join(parts)
        sys.stdout.write("\r" + Fore.CYAN + line + Style.RESET_ALL + " " * 8)
        sys.stdout.flush()

    def close(self) -> None:
        self._open = False
        sys.stdout.write("\n")