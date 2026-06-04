# Strategy 01 Research Brief

## Strategy 01: MGC Absorption Reversal

This brief translates the current user request into a valid research plan.

## Requested Direction

- Market: Gold futures
- Instrument: `MGC`
- Session focus first: New York
- Setup family: absorption reversal / failed continuation after aggressive pressure
- Account context: `10,000` sim account
- Position sizing goal: dynamic micro sizing with compounding logic
- Frequency goal: at least `3` trades per day

## Honest Constraints

### 1. Current dataset is not a continuous two-year sample

The MGC package currently available in `ADAPTIVE` is split into four coverage blocks:

- `2024-06-03` to `2024-08-22`
- `2024-12-02` to `2025-03-12`
- `2025-06-03` to `2025-08-13`
- `2025-12-03` to `2026-01-07`

That means we cannot honestly claim we have one continuous recent six-month block ending near the current date of `2026-06-04`, and we cannot honestly run a true one-year out-of-sample test after a most-recent six-month training window with the current package.

### 2. Minimum trade frequency and extreme compounding are targets, not assumptions

- We can optimize toward `3` or more trades per day, but the data must prove whether that frequency is compatible with edge after costs.
- We cannot responsibly assume a path from `10,000` to hundreds of thousands or millions in a year. That is an aspiration, not a validated planning input.

### 3. Drawdown and dynamic sizing should be imposed after signal quality is measured

The strategy edge must be tested first. Position-sizing rules for a `10,000` account should then be layered on top of validated trade distributions.

## Recommended Legitimate Plan

### Phase 1

Build and test the absorption-reversal event detector on the available MGC tick data with New York session only.

### Phase 2

Measure:

- trades per day
- win rate
- average favorable excursion
- average adverse excursion
- drawdown
- sensitivity to cost assumptions

### Phase 3

Add a conservative dynamic micro-sizing layer for a `10,000` account that explicitly targets low drawdown rather than assuming aggressive compounding is safe.

## First Strategy Thesis

When aggressive trade flow pushes into a key New York session liquidity area but price fails to continue and instead rejects back, the pressure may have been absorbed and late traders may be trapped. If price rotates away from that failed area, there may be a short-term reversal opportunity.

## Immediate Build Target

Create the first absorption-reversal event detector for New York session only on MGC tick data, then backtest it with conservative cost assumptions and no exaggerated performance claims.
