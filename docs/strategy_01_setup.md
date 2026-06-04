# Strategy 01 Setup

## Strategy

- Name: `Strategy 01: MGC Absorption Reversal`
- Session focus: New York only
- Dataset: local MGC tick package

## Current Logic

- Aggregate raw MGC trades into New York session second-bars
- Track rolling session extremes plus the first `30` minutes opening range
- Flag absorption candidates when signed flow and relative volume expand but price progress stays compressed
- Require sweep-and-reclaim behavior around the active session/opening-range boundary before entry
- Simulate fixed stop, fixed target, and time-stop exits net of commission and slippage
- Apply dynamic contract sizing with a hard cap derived from a `5%` drawdown budget on a `10,000` starting balance

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
