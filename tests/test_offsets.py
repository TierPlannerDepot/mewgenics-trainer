from pathlib import Path

from mewgenics_trainer.core.offsets import OffsetTable, _DEFAULTS


def test_defaults_loaded_when_missing(tmp_path: Path):
    missing = tmp_path / "nope.toml"
    table = OffsetTable.load(missing)
    assert table.gold == _DEFAULTS["gold"]
    assert table.stats["str"] == 0x0


def test_load_from_file(tmp_path: Path):
    cfg = tmp_path / "current.toml"
    cfg.write_text(
        "[gold]\nchain = [1, 2, 3]\n\n"
        "[stats]\nchain = [4]\nstr = 0\ndex = 4\nint = 8\ncon = 12\n\n"
        "[cats]\nchain = [5]\ncount = 0\nfirst = 8\nstride = 0x100\n"
    )
    table = OffsetTable.load(cfg)
    assert table.gold["chain"] == [1, 2, 3]
    assert table.cats["stride"] == 0x100