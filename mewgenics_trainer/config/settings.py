"""Load trainer settings from TOML or defaults."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import tomli

_DEFAULT_PATH = Path.home() / ".mewgenics-trainer" / "config.toml"


@dataclass
class TrainerSettings:
    tick_interval: float = 0.1
    disable_overlay: bool = False
    gold_cap: int = 999_999
    stat_cap: int = 99
    auto_apply_stats: bool = False
    feature_flags: dict = field(default_factory=dict)


def load_settings(path: str | None = None) -> TrainerSettings:
    target = Path(path) if path else _DEFAULT_PATH
    if not target.exists():
        return TrainerSettings()
    with target.open("rb") as fh:
        data = tomli.load(fh).get("trainer", {})
    return TrainerSettings(**{k: v for k, v in data.items() if k in TrainerSettings.__dataclass_fields__})