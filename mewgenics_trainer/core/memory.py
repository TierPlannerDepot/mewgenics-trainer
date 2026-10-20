"""Thin wrapper around pymem with safe read/write helpers."""
from __future__ import annotations

import struct
from typing import Optional

import pymem
import pymem.process
from pymem.exception import ProcessNotFound, CouldNotOpenProcess

from ..utils.logger import get_logger

log = get_logger("memory")


class ProcessMemory:
    def __init__(self, process_name: str) -> None:
        self.process_name = process_name
        self.pid: Optional[int] = None
        self.base: Optional[int] = None
        self._pm: Optional[pymem.Pymem] = None

    def attach(self) -> bool:
        try:
            self._pm = pymem.Pymem(self.process_name)
        except (ProcessNotFound, CouldNotOpenProcess) as exc:
            log.debug("attach failed: %s", exc)
            return False
        self.pid = self._pm.process_id
        module = pymem.process.module_from_name(self._pm.process_handle, self.process_name)
        if module is None:
            log.warning("module %s not found in target", self.process_name)
            return False
        self.base = module.lpBaseOfDll
        return True

    def detach(self) -> None:
        if self._pm:
            try:
                self._pm.close_process()
            except Exception:
                pass
        self._pm = None
        self.pid = None
        self.base = None

    def read_int(self, address: int) -> int:
        assert self._pm is not None
        return struct.unpack("<i", self._pm.read_bytes(address, 4))[0]

    def write_int(self, address: int, value: int) -> None:
        assert self._pm is not None
        self._pm.write_bytes(address, struct.pack("<i", value), 4)

    def read_float(self, address: int) -> float:
        assert self._pm is not None
        return struct.unpack("<f", self._pm.read_bytes(address, 4))[0]

    def read_pointer(self, address: int) -> int:
        assert self._pm is not None
        return struct.unpack("<Q", self._pm.read_bytes(address, 8))[0]

    def resolve_chain(self, base: int, offsets: list[int]) -> int:
        ptr = self.read_pointer(base)
        for off in offsets[:-1]:
            ptr = self.read_pointer(ptr + off)
        return ptr + offsets[-1]