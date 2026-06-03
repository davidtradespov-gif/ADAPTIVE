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

## Next Build Step

Build the first event detector and leakage-safe backtest workflow for this setup.
