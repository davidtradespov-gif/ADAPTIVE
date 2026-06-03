# Project Memory

Last updated: 2026-06-04 09:03 +10:00

## Purpose

This file stores durable project memory for `ADAPTIVE` so future sessions can resume work without relying on chat history.

## Decisions

- 2026-06-04: Initialized the project memory layer before any code existed in the repository.
- 2026-06-04: Standard memory files for this workspace are `MEMORY.md` and `PROJECT_STATE.md`.
- 2026-06-04: Every meaningful change should be reflected in repo memory, then committed to Git.
- 2026-06-04: `AGENTS.md` is part of the durable repo memory layer for future sessions.
- 2026-06-04: This workspace should use only the new GitHub remote `https://github.com/davidtradespov-gif/ADAPTIVE.git`.
- 2026-06-04: Accidental nested repo setup was removed so the project root is again `C:\Users\david\OneDrive - My Biologics Pty Ltd\Trading\ADAPTIVE`.
- 2026-06-04: The linked Obsidian vault is the repository root `C:\Users\david\OneDrive - My Biologics Pty Ltd\Trading\ADAPTIVE`.
- 2026-06-04: Obsidian persistence should center on the local `ADAPTIVE.md` hub note that acts as the project spiderweb node.
- 2026-06-04: The local Obsidian vault metadata now lives under `.obsidian` inside the project folder.
- 2026-06-04: The GitHub repository URL is reachable and appears to be a live empty repository.
- 2026-06-04: Git Credential Manager was re-authenticated to GitHub as `davidtradespov-gif`.

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
- 2026-06-04: Obsidian files should live inside the `ADAPTIVE` folder so they are stored with Git and project files.

## Known Gaps

- 2026-06-04: Git push to `https://github.com/davidtradespov-gif/ADAPTIVE.git` is still unverified because `git ls-remote` returned `Repository not found`.
- 2026-06-04: `git push -u origin main` still fails with `Repository not found`, so local commits cannot yet be published to GitHub.
- 2026-06-04: Older external-vault notes may still exist in `Documents\Obsidian Vault`, but the active project vault is now the repo root.

## Latest Outcome

- 2026-06-04: `git push -u origin main` succeeded after refreshing GitHub credentials to `davidtradespov-gif`.
