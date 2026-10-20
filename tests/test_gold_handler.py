from unittest.mock import MagicMock

from mewgenics_trainer.core.offsets import OffsetTable
from mewgenics_trainer.handlers.gold_handler import GoldHandler


def _fake_mem(current_gold: int):
    mem = MagicMock()
    mem.base = 0x140000000
    mem.resolve_chain.return_value = 0xDEADBEEF
    mem.read_int.return_value = current_gold
    return mem


def test_gold_handler_writes_when_below_target():
    mem = _fake_mem(100)
    handler = GoldHandler(mem, OffsetTable.load(), target=5000)
    handler.enable()
    handler.tick()
    mem.write_int.assert_called_once_with(0xDEADBEEF, 5000)


def test_gold_handler_skips_when_at_cap():
    mem = _fake_mem(999_999)
    handler = GoldHandler(mem, OffsetTable.load(), target=999_999)
    handler.enable()
    handler.tick()
    mem.write_int.assert_not_called()