# Strategy 01 Setup

## Strategy

- Name: `Strategy 01: MGC Absorption Reversal`
- Session focus: New York only
- Dataset: local MGC tick package

## Current Logic

- Aggregate raw MGC trades into New York session second-bars
- Track recent intraday extremes plus the first `30` minutes opening range
- Generate high-frequency sweep/rejection candidates using close location, signed-flow pressure, CVD-vs-price efficiency, and activity expansion
- Rank the candidate pool with a local probability model trained on the same training-window outcomes
- Select up to `30` distinct setups per day with cooldown spacing
- Simulate fixed stop, fixed target, time-stop, and opposite-pressure exits net of commission and slippage
- Apply dynamic contract sizing with a hard cap derived from a `20%` drawdown budget on a `10,000` starting balance

## Runner

```powershell
& 'C:\Users\david\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' `
  'C:\Users\david\OneDrive - My Biologics Pty Ltd\Trading\ADAPTIVE\scripts\strategy_01_absorption_reversal.py'
```

## Outputs

- `reports/strategy_01_absorption_reversal_report.json`
- `reports/strategy_01_absorption_reversal_report.md`

## Current Windowing

Because the current dataset is segmented, the current implementation uses:

- the last `180` available trading-day folders with parquet data as the training set

This is a practical working build choice on the available data, not a claim that the history is continuous.

## Current Reality Check

- The current high-frequency build gets very close to the requested `30` trades per day target on the full New York-session training run.
- It does not yet hold full-window drawdown under the requested `20%` cap, so this version is still a strategy-construction build rather than a finished deployable model.
