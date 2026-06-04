# Strategy 01 Research Brief

Backlink: [[ADAPTIVE]]

## Summary

This note stores the honest working brief for the first absorption-reversal strategy request.

## Requested Build

- `MGC`
- New York session first
- `10,000` sim-account design context
- dynamic micro sizing
- target of at least `3` trades per day

## Important Constraint

The current dataset is not one continuous two-year sequence. It is split into four date blocks, so a true "train on the last 6 months, then backtest 1 year OOS" workflow is not currently possible with the data package as it stands.

## Working Plan

1. Build the first New York session absorption-reversal event detector.
2. Backtest it honestly on the available MGC data.
3. Measure trade frequency and drawdown before applying compounding assumptions.
4. Add dynamic micro sizing only after the base signal is validated.
