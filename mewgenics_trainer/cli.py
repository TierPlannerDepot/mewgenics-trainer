"""Command-line entrypoint for mewgenics-trainer."""
from __future__ import annotations

import argparse
import sys
import time

from .bootstrap import TrainerSession
from .config.settings import load_settings
from .utils.logger import get_logger

log = get_logger("cli")


def _parse_args(argv: list[str]) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="mewtrainer", description="Mewgenics Trainer")
    p.add_argument("--process", default="Mewgenics.exe", help="target process name")
    p.add_argument("--config", default=None, help="path to trainer config TOML")
    p.add_argument("--attach-only", action="store_true", help="attach and dump module info, then exit")
    p.add_argument("--no-overlay", action="store_true", help="disable the on-screen overlay")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv if argv is not None else sys.argv[1:])
    settings = load_settings(args.config)

    session = TrainerSession(process_name=args.process, settings=settings)
    if not session.attach():
        log.error("could not attach to %s — is Mewgenics running?", args.process)
        return 2

    log.info("attached to %s (pid=%s, base=0x%x)", args.process, session.pid, session.base or 0)

    if args.attach_only:
        session.detach()
        return 0

    try:
        session.enable_all()
        while session.running:
            session.tick()
            time.sleep(settings.tick_interval)
    except KeyboardInterrupt:
        log.info("interrupt received, shutting down")
    finally:
        session.detach()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())