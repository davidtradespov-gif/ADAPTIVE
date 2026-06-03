# First Strategy Spec

## Strategy 01: MGC Failed Auction Reversal

This is the first independent Gold order-flow strategy thesis for `ADAPTIVE`.

It is a research specification, not a live trading rule.

## Why This Is A Good First Strategy

- It matches the stored order-flow education context.
- It uses concepts we can test with the current MGC tick trade dataset.
- It is simpler and easier to falsify than a broad multi-factor model.
- It fits a smaller live-account context better than wide-risk discretionary Gold trading.

## Product Context

- Instrument: `MGC` Micro Gold futures
- Contract size: `10 troy ounces`
- Minimum fluctuation: `$0.10 per troy ounce`
- Dollar value per tick: `$1.00 per contract`

These product details are based on CME’s Micro Gold contract information. Sources:
- [CME Micro Gold overview](https://www.cmegroup.com/education/courses/understanding-micro-futures-contracts-at-cme-group/micro-gold-and-silver-futures/micro-gold-and-micro-silver-futures-product-overview.html)
- [CME Micro Metals specs](https://www.cmegroup.com/markets/microsuite/metals.html)

## Live Account Context

Current design context:

- Target deployment context is a `10,000` live account.

Research implication:

- Start with a one-contract `MGC` mindset.
- Keep early live-risk assumptions conservative.
- Prefer clean invalidation and low operational complexity over large target seeking.

## Core Thesis

When price sweeps an obvious liquidity area in Gold but fails to continue, the move may reverse because late breakout traders become trapped and opposing participants absorb the aggressive pressure.

If price then reclaims or rejects back through the failed area and begins rotating away, there may be a short-term opportunity.

## Market Context

Study this setup around meaningful locations such as:

- prior session high or low
- overnight high or low
- opening range edge
- fresh session extreme
- equal highs or lows
- round-number areas

## Event Definition

An event candidate occurs when:

1. price pushes through a known liquidity level
2. continuation is weak or fails
3. price rejects and rotates back through or away from the swept area

## Confirmation Ideas To Test

The first backtest should evaluate combinations of:

- sweep distance beyond the level
- speed of rejection
- local trade-volume surge
- failure to continue after the surge
- price re-entry into the prior range
- short-horizon return after reclaim

Because the current dataset is trade ticks rather than full depth, the first version should avoid relying on DOM-only features.

## Invalidation Concept

The thesis is wrong if price accepts beyond the swept level and continues away rather than rejecting and rotating back.

## What To Build Next

1. Create a clean event detector for liquidity sweeps around prior session and intraday reference levels.
2. Build leakage-safe labels for reversal success versus failure.
3. Backtest the setup net of costs on the MGC dataset.
4. Review whether the edge is stable enough to justify a real live-account risk model for a `10,000` account.
