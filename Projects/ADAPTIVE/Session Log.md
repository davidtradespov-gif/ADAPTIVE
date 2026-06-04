# ADAPTIVE Session Log

Backlink: [[ADAPTIVE]]

## 2026-06-04

- Initialized project memory scaffolding in the repo.
- Removed the accidental nested repository and rebuilt a clean root repo.
- Added a repo runbook to enforce repo, Obsidian, and Git persistence together.
- Created a local Obsidian vault structure inside the project folder.
- Created the `[[ADAPTIVE]]` hub note and linked supporting notes to establish a graph node.
- Verified that the configured GitHub remote currently returns `Repository not found`.
- Re-tested after the repository was made public; reachability is fixed, but push now fails with `403 Permission denied to smilefounders-dev`.
- Refreshed Git Credential Manager authentication to `davidtradespov-gif`.
- Pushed `main` successfully to `origin/main`.
- Recorded a permanent rule that `davidtradespov-gif` is the only allowed GitHub identity and push target for this project.
- Recorded the MGC COMEX historical trade package as the canonical Gold research dataset and added project research rules.
- Stored the full provided order-flow education context inside the local Obsidian vault.
- Installed local parquet support, created a reusable MGC audit script, and generated the first audit report.
- Recorded that the current requirement is simply that the stored MGC tick data is available for backtesting.
- Defined the first strategy thesis as an MGC failed-auction reversal setup for a `10,000` live-account design context.
- Added an honest research brief for the requested absorption-reversal build and documented the current data continuity limitation.
- Built and ran the first executable New York-session absorption-reversal runner on the last 180 available MGC day folders.
- The first run generated many trades but did not meet the 10k / 5% drawdown objective even at one contract.
- Reworked Strategy 01 around opening-range and session-extreme sweep context, rolling signed-flow absorption, reclaim confirmation, and conservative costed exits.
- Re-ran the strengthened Strategy 01 build across the last 180 available day folders and finalized a training version that reached exactly `3.00` trades per day with about `4.66%` max drawdown on the 10k simulation.
- Built a separate high-frequency New York-session Strategy 01 variant using sweep/rejection candidate generation, pressure features, probability ranking, and top-quality daily selection toward `30` trades per day.
- Verified that the high-frequency build reaches about `29.85` trades per day on the full 180-day training run, but it still carries about `36.15%` max drawdown and is not yet inside the requested `20%` ceiling.
- Reworked the high-frequency exit architecture into a managed model with hard stop, break-even promotion, trailing stop activation, runner hold/trail logic, time exit, session flatten, and opposite-pressure exits.
- Finalized a full-window high-frequency training build at about `29.85` trades per day, about `$117103.00` net PnL, and about `18.74%` max drawdown on the `10,000` simulation.

## 2026-06-05

- Ran a full continuity audit on this laptop after migrating the project away from the prior OneDrive-based location.
- Confirmed the local repo contains the expected memory files, Obsidian notes, MGC dataset, strategy scripts, and generated reports.
- Confirmed the configured Git remote remains only `https://github.com/davidtradespov-gif/ADAPTIVE.git`.
- Confirmed the local Obsidian vault metadata and linked project notes are present inside this folder.
- Re-baselined project memory, setup docs, and linked notes to `C:\Users\smile\Documents\ADAPTIVE LOCAL BASED\ADAPTIVE` as the new authoritative project path.
- Confirmed GitHub fetch and push both work from this laptop after correcting the shell context so Git Credential Manager can locate `git.exe`.
