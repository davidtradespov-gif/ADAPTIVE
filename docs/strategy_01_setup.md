# Strategy 01 Setup

## Strategy

- Name: `Strategy 01: MGC Absorption Reversal`
- Session focus: New York only
- Dataset: local MGC tick package

## Current Logic

- Aggregate raw MGC trades into session-specific second-bars across Asia, London, and New York
- Track recent intraday extremes plus each session opening range
- Generate high-frequency sweep/rejection candidates using close location, signed-flow pressure, CVD-vs-price efficiency, activity expansion, and session context
- Rank the candidate pool with a local probability model trained on the same training-window outcomes
- Select the best cross-session opportunities globally each trade day inside a `25-50` trades/day search band
- Simulate managed exits with a hard stop, break-even promotion, trailing stop activation, runner hold/trail logic, time exits, session flatten, and opposite-pressure exits net of commission and slippage
- Apply dynamic contract sizing with a hard cap derived from a `20%` drawdown budget on a `10,000` starting balance

## Runner

```powershell
$env:PYTHONPATH = ".python_packages"
& 'C:\Users\smile\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' .\scripts\strategy_01_absorption_reversal.py
```

## Outputs

- `reports/strategy_01_absorption_reversal_report.json`
- `reports/strategy_01_absorption_reversal_report.md`

## Current Windowing

Because the current dataset is segmented, the current implementation uses:

- the last `180` available trading-day folders with parquet data as the training set

This is a practical working build choice on the available data, not a claim that the history is continuous.

## Current Reality Check

- The accepted V2 build uses all three sessions and a global daily selector, with the best under-ceiling training variant landing at about `39.87` trades per day, about `$160,292.10` net PnL, and about `18.22%` max drawdown on a `10,000` starting balance.
- The `45` and `50` trades/day V2 variants made more gross training PnL but breached the drawdown ceiling and are not the accepted baseline.
- The probability selector is still trained on the same 180-day candidate pool, so this is still a strategy-construction result and still needs true chronological validation before any live claim.
