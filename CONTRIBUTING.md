# Contributing to mewgenics-trainer

Thanks for helping keep the trainer working after each Mewgenics patch.

## Workflow

1. Fork the repo and create a feature branch from `main`.
2. Run `pip install -r requirements.txt` in a virtualenv.
3. Refresh offsets with `python -m tools.update_offsets` against the current build.
4. Run `pytest -q` before opening a PR.

## Offset PRs

Please include:

- The Mewgenics build string (from the title screen).
- The signature or pointer chain you used to derive the offset.
- A short note on what changed vs. `offsets/current.toml`.

## Handler rules

- Handlers live in `mewgenics_trainer/handlers/` and must subclass `BaseHandler`.
- Never busy-loop; use the `tick_interval` from settings.
- Wrap reads in try/except — the target may detach or the pointer may go stale.

## Feature requests

Open an issue first. Features that require injecting a DLL into Mewgenics are
out of scope for this repo; this trainer is external-memory only.