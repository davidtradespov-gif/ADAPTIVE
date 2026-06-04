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

The current high-frequency research variant uses:

- New York session only
- second-bar aggregation from the MGC tick stream
- recent intraday sweep / stop-run context
- close-location rejection logic
- CVD and signed-flow pressure-efficiency features
- volume-burst / activity-expansion features
- score-based candidate generation
- a local probability model to rank the candidate pool
- cooldown spacing and top-quality daily selection toward a `30` trades/day target
- managed exits with hard stop, break-even promotion, trailing stop activation, runner hold/trail logic, time exit, session flatten, opposite-pressure exit, commission, and slippage
- dynamic contract sizing capped by a `20%` starting-balance drawdown budget

## Continuity Checkpoint

- Canonical local script: `scripts/strategy_01_absorption_reversal.py`
- Canonical local report: `reports/strategy_01_absorption_reversal_report.md`
- Canonical checkpoint reference: commit `3fef09a` for the managed-exit high-frequency build
- Continuity audit status on 2026-06-05: local files match the expected managed-exit high-frequency build, so no missing strategy logic had to be reconstructed

## Current Result

- A strengthened executable runner now exists for this setup.
- On the last `180` available MGC parquet day folders, New York session only, the current build produced `273` trades and exactly `3.00` trades per day.
- Win rate was about `82.42%`.
- Net PnL was about `$7580.70` on the `10,000` training simulation.
- Max drawdown was about `$465.90`, which is about `4.66%` of starting balance.
- The current version now satisfies both the drawdown requirement and the minimum `3` trades per day target on the training window.

## High-Frequency Result

- The high-frequency New York-session build on the last `180` available MGC parquet day folders produced `5,493` selected trades and about `29.85` trades per day.
- Win rate was about `79.92%`.
- Net PnL was about `$117103.00` on the `10,000` training simulation.
- Max drawdown was about `$1874.30`, which is about `18.74%` of starting balance.
- This means the current high-frequency managed-exit build now fits the requested training-window target envelope while still needing true chronological validation before any live claim.

## Current Limitation

- The probability selector is still trained on the same `180`-day candidate pool used for selection, so the current result is a strategy-construction training result, not true validation or OOS evidence.

## Next Exact Build Step

- Freeze the current high-frequency managed-exit training configuration and add the first true chronological validation block before changing the strategy design.
