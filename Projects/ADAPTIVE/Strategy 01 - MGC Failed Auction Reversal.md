# Strategy 01 - MGC Failed Auction Reversal

Backlink: [[ADAPTIVE]]

## Summary

This is the first Gold strategy thesis for the project.

It is based on:

- liquidity sweep
- failed auction
- rejection
- trapped traders

## Why This First

- It fits the stored order-flow research framework.
- It can be tested with the available MGC tick trade dataset.
- It is easier to falsify than a larger multi-factor strategy.
- It fits a `10,000` live-account design context better than wide-risk discretionary Gold trading.

## Product Context

- Instrument: `MGC`
- Contract size: `10 troy ounces`
- Tick size: `$0.10 per troy ounce`
- Tick value: `$1.00 per contract`

## Thesis

When Gold sweeps an obvious liquidity level but fails to continue, trapped breakout traders may help fuel a reversal back away from that level.

## Research Direction

Test the setup around:

- prior session high or low
- overnight high or low
- opening range edge
- fresh session extremes
- equal highs or lows

## Current Build

The current executable build uses:

- New York session only
- second-bar aggregation from the MGC tick stream
- prior session-extreme and opening-range sweep context
- rolling signed-flow and relative-volume absorption filters
- reclaim confirmation before entry
- fixed stop, fixed target, time stop, commission, and slippage
- dynamic contract sizing capped by a `5%` starting-balance drawdown budget

## High-Frequency Variant

The current high-frequency V2 research variant uses:

- Asia, London, and New York sessions
- session-specific second-bar aggregation from the MGC tick stream
- recent intraday sweep / stop-run context
- close-location rejection logic
- CVD and signed-flow pressure-efficiency features
- volume-burst / activity-expansion features
- score-based candidate generation
- a local probability model to rank the candidate pool
- `session_code` as part of the model feature set
- cooldown spacing and top-quality global cross-session daily selection inside a `25-50` trades/day search band
- managed exits with hard stop, break-even promotion, trailing stop activation, runner hold/trail logic, time exit, session flatten, opposite-pressure exit, commission, and slippage
- dynamic contract sizing capped by a `20%` starting-balance drawdown budget

## Continuity Checkpoint

- Canonical local script: `scripts/strategy_01_absorption_reversal.py`
- Canonical local report: `reports/strategy_01_absorption_reversal_report.md`
- Canonical checkpoint reference: commit `3fef09a` for the managed-exit high-frequency build
- Continuity audit status on 2026-06-05: local files match the expected managed-exit high-frequency build, so no missing strategy logic had to be reconstructed
- Current active checkpoint on 2026-06-08: V2 accepted baseline is the three-session `40`-target training build

## Current Result

- A strengthened executable runner now exists for this setup.
- On the last `180` available MGC parquet day folders, New York session only, the current build produced `273` trades and exactly `3.00` trades per day.
- Win rate was about `82.42%`.
- Net PnL was about `$7580.70` on the `10,000` training simulation.
- Max drawdown was about `$465.90`, which is about `4.66%` of starting balance.
- The current version now satisfies both the drawdown requirement and the minimum `3` trades per day target on the training window.

## High-Frequency Result

- The accepted V2 three-session build on the last `180` available MGC parquet day folders produced `7,137` selected trades and about `39.87` trades per day.
- Win rate was about `81.42%`.
- Net PnL was about `$160292.10` on the `10,000` training simulation.
- Max drawdown was about `$1822.00`, which is about `18.22%` of starting balance.
- The strongest selected opportunities came mostly from Asia and London, with far fewer surviving from New York once all sessions were ranked together.
- This means the current accepted V2 build improves materially on the old New York-only training result while still needing true chronological validation before any live claim.

## Current Limitation

- The probability selector is still trained on the same `180`-day candidate pool used for selection, so the current result is a strategy-construction training result, not true validation or OOS evidence.
- The current annualized training run-rate is about `$224408.94`, so the stated `$1,000,000` yearly target is not yet supported honestly by validated evidence.

## Next Exact Build Step

- Freeze the accepted V2 `40`-target three-session training configuration and add the first true chronological validation block before changing the strategy design.
