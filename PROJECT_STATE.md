# Project State

Last updated: 2026-06-04 09:42 +10:00

## System Summary

`ADAPTIVE` is initialized as a workspace with project memory scaffolding at the project root, but no application code or runtime components exist yet.

## Current Status

- Working: durable repo memory layer exists via `AGENTS.md`, `MEMORY.md`, and `PROJECT_STATE.md`
- Working: workspace path confirmed as `C:\Users\david\OneDrive - My Biologics Pty Ltd\Trading\ADAPTIVE`
- Working: old accidental nested repository has been removed
- Working: clean Git repository exists at the project root
- Working: `origin` is configured only as `https://github.com/davidtradespov-gif/ADAPTIVE.git`
- Working: Obsidian vault now lives inside `C:\Users\david\OneDrive - My Biologics Pty Ltd\Trading\ADAPTIVE`
- Working: local Obsidian graph hub exists at `ADAPTIVE.md`
- Working: local Obsidian vault metadata exists under `.obsidian`
- Working: the GitHub repo URL is now reachable
- Working: local GitHub authentication now uses `davidtradespov-gif`
- Working: `main` has been pushed to `origin/main`
- Working: project memory now explicitly forbids any push target other than `davidtradespov-gif/ADAPTIVE`
- Working: local commits `5119a8c` and `9fdf6b2` capture the current project setup and Obsidian sync workflow
- Working: the canonical MGC Gold tick dataset is stored locally inside the project folder
- Working: `DATASETS.md` and `RESEARCH_PRINCIPLES.md` define the Gold research baseline
- Working: `scripts/audit_mgc_dataset.py` can generate repeatable MGC audit reports
- Working: the first strategy research spec exists for `Strategy 01: MGC Failed Auction Reversal`
- Working: an explicit research brief exists for the requested absorption-reversal build
- Not started: codebase structure
- Not started: runtime environment
- Not started: tests, scripts, or deployment workflow
- In progress: Obsidian note synchronization target and hub structure

## Latest Validated State

- 2026-06-04: The project folder existed but was empty before setup.
- 2026-06-04: No existing memory files, README, runbook, or source files were present.
- 2026-06-04: An accidental nested `ADAPTIVE\ADAPTIVE` repo was created during setup and then removed.
- 2026-06-04: Temporary Git metadata at the project root was also removed so a clean repo can be created.
- 2026-06-04: A new clean root repository was initialized and connected only to `https://github.com/davidtradespov-gif/ADAPTIVE.git`.
- 2026-06-04: The project-local Obsidian vault was created inside the repo root.
- 2026-06-04: `git ls-remote` against the configured GitHub URL failed with `Repository not found`.
- 2026-06-04: `git push -u origin main` also failed with `Repository not found`.
- 2026-06-04: Commit `5db4aa5` moved the active Obsidian vault structure into the project folder.
- 2026-06-04: `git ls-remote` to `https://github.com/davidtradespov-gif/ADAPTIVE.git` succeeded after the repo was made public.
- 2026-06-04: `git push -u origin main` failed with `403 Permission denied to smilefounders-dev`.
- 2026-06-04: Git Credential Manager was refreshed and stored `git:https://github.com` for user `davidtradespov-gif`.
- 2026-06-04: `git push -u origin main` succeeded and established upstream tracking for `main`.
- 2026-06-04: MGC package metadata confirmed 204 day folders spanning `2024-06-03` to `2026-01-07`.
- 2026-06-04: First audit report confirmed 19,701,740 kept rows, six empty day folders, all-null `channel`, and a suspicious minimum price of `-333.0`.
- 2026-06-04: First strategy direction chosen: failed-auction reversal around swept liquidity levels in MGC Gold.
- 2026-06-04: Current dataset continuity does not support a true last-6-month train plus 1-year OOS workflow.

## Immediate Next Steps

1. Build the first New York-session absorption-reversal event detector on MGC.
2. Create leakage-safe labels and a conservative backtest workflow on the stored MGC tick data.
3. Measure realistic trade frequency and drawdown before adding dynamic compounding logic.

## Open Questions

- How should we define the first liquidity-sweep event detector for `Strategy 01`?
