# Project Memory

Last updated: 2026-06-08 11:40 +10:00

Related: [[ADAPTIVE]] | [[PROJECT_STATE]] | [[README]] | [[RUNBOOK]]

## Purpose

This file stores durable project memory for `ADAPTIVE` so future sessions can resume work without relying on chat history.

## Decisions

- 2026-06-04: Initialized the project memory layer before any code existed in the repository.
- 2026-06-04: Standard memory files for this workspace are `MEMORY.md` and `PROJECT_STATE.md`.
- 2026-06-04: Every meaningful change should be reflected in repo memory, then committed to Git.
- 2026-06-04: `AGENTS.md` is part of the durable repo memory layer for future sessions.
- 2026-06-04: This workspace should use only the new GitHub remote `https://github.com/davidtradespov-gif/ADAPTIVE.git`.
- 2026-06-04: Accidental nested repo setup was removed so the project root is again `C:\Users\smile\Documents\ADAPTIVE LOCAL BASED\ADAPTIVE`.
- 2026-06-04: The linked Obsidian vault is the repository root `C:\Users\smile\Documents\ADAPTIVE LOCAL BASED\ADAPTIVE`.
- 2026-06-04: Obsidian persistence should center on the local `ADAPTIVE.md` hub note that acts as the project spiderweb node.
- 2026-06-04: The local Obsidian vault metadata now lives under `.obsidian` inside the project folder.
- 2026-06-04: The GitHub repository URL is reachable and appears to be a live empty repository.
- 2026-06-04: Git Credential Manager was re-authenticated to GitHub as `davidtradespov-gif`.
- 2026-06-04: Gold strategy research begins with `MGC` COMEX historical trade tick data stored locally inside this project.
- 2026-06-04: The active MGC package root is `C:\Users\smile\Documents\ADAPTIVE LOCAL BASED\ADAPTIVE\mgc_comex_trades_package (2)\mgc_comex_trades_package`.
- 2026-06-04: Independent order-flow research is allowed; proprietary copied strategy logic is not.
- 2026-06-04: A reusable MGC audit workflow now exists at `scripts/audit_mgc_dataset.py`.
- 2026-06-04: The first strategy thesis is `Strategy 01: MGC Failed Auction Reversal`.
- 2026-06-04: The first live-account design context is a `10,000` account with an initial one-contract `MGC` mindset.
- 2026-06-04: The first user-requested implementation direction is an absorption-reversal strategy for New York session in MGC.
- 2026-06-04: A first executable Strategy 01 runner now exists at `scripts/strategy_01_absorption_reversal.py`.
- 2026-06-04: The current high-frequency Strategy 01 build uses New York session second-bars, recent intraday sweep context, opening-range context bonus, signed-flow/CVD pressure features, score-based selection, a local probability model, managed trailing/runner exits, net costs, and dynamic contract sizing capped by a 20% starting-balance drawdown budget.

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
- 2026-06-04: Never ever push this project to any GitHub account other than `davidtradespov-gif`.
- 2026-06-04: `davidtradespov-gif` is the only permitted GitHub identity and remote owner for `ADAPTIVE`.
- 2026-06-04: Use the stored MGC historical package as the default test bed for all Gold strategies unless replaced by a newer recorded dataset.
- 2026-06-04: For the current phase, the important point is that the MGC tick data is present and usable for backtesting.

## Known Gaps

- 2026-06-04: Older external-vault notes may still exist in `Documents\Obsidian Vault`, but the active project vault is now the repo root.
- 2026-06-04: The initial audit is complete, but the `-333.0` minimum price and the spread-versus-outright ticker policy still need resolution.
- 2026-06-04: The first audit found six empty day folders, all-null `channel` values, and a suspicious minimum `price` of `-333.0` that must be explained before live research assumptions are trusted.
- 2026-06-04: The current MGC package is not a continuous two-year sample, so a true "last 6 months train then 1 year OOS" split is not currently possible.
- 2026-06-04: The current high-frequency Strategy 01 build now fits the requested training-window envelope, producing about `29.85` trades per day with about `18.74%` max drawdown on the full 180-day New York-session run.

## Latest Outcome

- 2026-06-04: `git push -u origin main` succeeded after refreshing GitHub credentials to `davidtradespov-gif`.
- 2026-06-04: The first full MGC audit report was generated successfully after installing local `pyarrow` support into `.python_packages`.
- 2026-06-04: A first Gold strategy research spec was created using a failed-auction reversal thesis.
- 2026-06-04: The first executable Strategy 01 report was generated in `reports/strategy_01_absorption_reversal_report.md`.
- 2026-06-04: The stable low-frequency Strategy 01 build on the last 180 available day folders produced `273` trades, exactly `3.00` trades per day, `82.42%` win rate, `$7580.70` net PnL, and about `4.66%` max drawdown on a `10,000` starting balance with dynamic sizing capped at `3` contracts.
- 2026-06-04: The current high-frequency Strategy 01 build targeting about `30` trades per day produced `5,493` selected New York-session trades, about `29.85` trades per day, `79.92%` win rate, `$117103.00` net PnL, and about `18.74%` max drawdown on the full 180-day training run.
- 2026-06-05: A full continuity audit on this laptop confirmed the local repo, Obsidian vault, MGC dataset, strategy scripts, and reports are present, and the project memory layer was re-baselined to `C:\Users\smile\Documents\ADAPTIVE LOCAL BASED\ADAPTIVE`.
- 2026-06-05: GitHub fetch and push both succeeded from this laptop against `https://github.com/davidtradespov-gif/ADAPTIVE.git` after ensuring Git Credential Manager could see `git.exe` on `PATH`.
- 2026-06-05: This laptop path `C:\Users\smile\Documents\ADAPTIVE LOCAL BASED\ADAPTIVE` is now the authoritative project baseline and old machine-specific path references should be removed from repo memory, Obsidian notes, and setup docs.
- 2026-06-05: Continuity audit confirmed the local `scripts/strategy_01_absorption_reversal.py` and `reports/strategy_01_absorption_reversal_report.md` fully contain the managed-exit high-frequency Strategy 01 checkpoint associated with commit `3fef09a`, with no missing strategy reconstruction required.
- 2026-06-08: Strategy 01 V2 was extended across Asia, London, and New York using the same absorption-reversal logic family with a global cross-session daily selector.
- 2026-06-08: The best full 180-day training variant that stayed inside the `20%` drawdown ceiling was the `40` trades/day target, producing `7,137` trades, about `39.87` trades/day, `81.42%` win rate, about `$160292.10` net PnL, and about `18.22%` max drawdown on the `10,000` simulation.
- 2026-06-08: The `45` and `50` trades/day V2 variants produced higher training PnL but exceeded the drawdown ceiling at about `20.04%` and `21.75%`, so they are not the current accepted baseline.
- 2026-06-08: The V2 annualized run-rate from the segmented training window is about `$224408.94`, which improves materially on the prior New York-only build but does not honestly justify a `$1,000,000` yearly claim yet.
- 2026-06-08: A contract-unit audit found that the backtester had been mixing raw MGC price deltas with tick counts, so older Strategy 01 reports materially mis-stated both exits and dollar PnL and should not be treated as trusted evidence.
- 2026-06-08: After correcting MGC math to use `0.10` price ticks and `$1.00` tick value, a clean rerun of the accepted 180-day V2 `40`-target baseline with `base_runner_9` produced `7,137` trades, about `39.87` trades/day, `36.77%` win rate, about `$2902680.60` net PnL, and about `19.28%` max drawdown on the `10,000` simulation, with selected trades shifting toward London (`3,599`) and New York (`1,036`) relative to the pre-fix report.

## Consolidated Strategy 01 Checkpoint

- 2026-06-05: Canonical local strategy state is `Strategy 01: MGC New York-session absorption reversal`.
- 2026-06-05: Thesis remains a failed-auction / absorption-reversal idea after a recent intraday sweep or stop-run where aggressive pressure fails to continue and price rejects back.
- 2026-06-05: The active high-frequency build uses New York session second-bars, recent intraday sweep context, close-location rejection logic, signed-flow and short-horizon CVD pressure features, activity expansion via relative size, opening-range context bonus, probability-style candidate ranking, cooldown spacing, and top-quality daily selection toward `30` trades/day.
- 2026-06-05: The active managed exits are hard stop, break-even promotion, trailing-stop activation, runner activation, runner trail distance, session flatten, time exit, and opposite-pressure exit.
- 2026-06-05: Dynamic sizing is still balance-based but effectively capped at `1` contract in the current report because the one-contract training drawdown already consumes most of the `20%` starting-balance drawdown budget.
- 2026-06-05: Current reported training result on the last `180` available parquet day folders is `5,493` trades, about `29.85` trades/day, `79.92%` win rate, about `$117103.00` net PnL, and about `18.74%` max drawdown on a `10,000` simulation.
- 2026-06-05: Honesty constraint remains unchanged: the probability selector is trained on the same `180`-day candidate pool used for selection, so this is still a strategy-construction result and not true chronological validation or OOS evidence.
- 2026-06-05: The next exact build step is to freeze this training configuration and add the first true chronological validation block before any redesign or extension.
- 2026-06-08: Canonical active strategy state is now `Strategy 01 V2: MGC absorption reversal across Asia, London, and New York with global daily selection`.
- 2026-06-08: Session definitions currently used are Asia `20:00-01:00`, London `02:00-08:00`, and New York `08:00-13:00` in New York time.
- 2026-06-08: V2 keeps the same core event logic but adds `session_code` to the model feature set and ranks all three sessions together each trade day instead of selecting only inside New York.
- 2026-06-08: The pre-fix V2 checkpoint that showed about `$160292.10` net and `81.42%` win rate is no longer trustworthy because it was generated before the MGC contract-unit correction.
- 2026-06-08: The current corrected V2 `40`-target rerun uses `base_runner_9`, selects `2,502` Asia trades, `3,599` London trades, and `1,036` New York trades, and currently shows no runner-qualified trades because the same-window probability model now scores all selected candidates below the current runner threshold.
- 2026-06-08: The next exact build step is now to freeze the corrected V2 `40`-target configuration and run the first true chronological validation block before any more parameter expansion or live-use discussion.

## Research Guardrails

- Use order-flow education and first-principles market microstructure only.
- Do not reconstruct private strategy rules, thresholds, exits, sizing models, or execution behavior from another system.
- Use chronological splits, conservative fills, and net-of-cost testing for all MGC research.
