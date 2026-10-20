# Security Policy

## Supported versions

Only the latest tagged release receives offset updates. Older tags are archived.

## Reporting a vulnerability

This project attaches to a user's own Mewgenics process and reads/writes its
memory. If you find a bug that could cause unintended writes (e.g. corrupting
save data or crashing the target), please report it privately:

- Email: security@mewgenics-trainer.example
- Do not open a public issue for memory-safety bugs.

## Scope

- In scope: out-of-bounds writes, unsafe pointer chains, privilege escalation
  via the attach helper.
- Out of scope: bans issued by Mewgenics' anti-cheat, distribution of compiled
  binaries, or use against other players' processes.

## Warnings

This trainer is for **single-player / offline use only**. Using it online can
get your account banned. You are responsible for how you use it.