# Project Memory

Last updated: 2026-06-04 08:45 +10:00

## Purpose

This file stores durable project memory for `ADAPTIVE` so future sessions can resume work without relying on chat history.

## Decisions

- 2026-06-04: Initialized the project memory layer before any code existed in the repository.
- 2026-06-04: Standard memory files for this workspace are `MEMORY.md` and `PROJECT_STATE.md`.
- 2026-06-04: Every meaningful change should be reflected in repo memory, then committed to Git.
- 2026-06-04: `AGENTS.md` is part of the durable repo memory layer for future sessions.
- 2026-06-04: This workspace should use only the new GitHub remote `https://github.com/davidtradespov-gif/ADAPTIVE.git`.
- 2026-06-04: Accidental nested repo setup was removed so the project root is again `C:\Users\david\OneDrive - My Biologics Pty Ltd\Trading\ADAPTIVE`.
- 2026-06-04: The linked Obsidian vault is `C:\Users\david\OneDrive - My Biologics Pty Ltd\Documents\Obsidian Vault`.
- 2026-06-04: Obsidian persistence should center on a linked `ADAPTIVE` hub note that acts as the project spiderweb node.

## Operational Rules

- Read `MEMORY.md` and `PROJECT_STATE.md` at the start of each session before making assumptions.
- Record durable instructions, decisions, bugs, fixes, and next steps here during the session rather than only in chat.
- Preserve useful historical context while keeping entries concrete and low-noise.
- Do not commit unrelated user changes.
- Commit meaningful project changes with clear messages.

## User Preferences

- 2026-06-04: This workspace should be set up with durable project memory from the start.
- 2026-06-04: Do not refer to, connect to, or use any old GitHub repository for this project.
- 2026-06-04: Every meaningful project change should be mirrored into Obsidian as well as the repo and Git history.

## Known Gaps

- 2026-06-04: Git push to `https://github.com/davidtradespov-gif/ADAPTIVE.git` is still unverified because `git ls-remote` returned `Repository not found`.
- 2026-06-04: `git push -u origin main` still fails with `Repository not found`, so local commits cannot yet be published to GitHub.
