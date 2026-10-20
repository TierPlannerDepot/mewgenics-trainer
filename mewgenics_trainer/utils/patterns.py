"""Signature-scan helpers used when offsets need refreshing."""
from __future__ import annotations

import re
from typing import Optional


def compile_sig(sig: str) -> re.Pattern[bytes]:
    parts = sig.strip().split()
    pattern = b"".join(b"." if p in ("??", "?") else re.escape(bytes([int(p, 16)])) for p in parts)
    return re.compile(pattern, re.DOTALL)


def find_in_blob(blob: bytes, sig: str) -> Optional[int]:
    m = compile_sig(sig).search(blob)
    return m.start() if m else None