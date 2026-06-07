# Strategy 01 Absorption Reversal Report

## Scope

- Instrument: `MGC`
- Sessions: `Asia, London, New York`
- Setup family: absorption reversal / failed continuation
- Account context: `10,000` sim
- Strategy target band: `25` to `50` trades per day with max `20%` drawdown

## Important Honesty Note

This report uses the segmented MGC dataset currently available in the repository. It is not a claim of a continuous recent six-month train plus one-year OOS sample.
The probability selector is still fit on the same candidate pool used to rank opportunities in this run, so this remains a strategy-construction result rather than a true validation result.

## V2 Search Outcome

- Selected trade target: `40` per day
- Average realized trades per day: `39.87`
- Net PnL: `$160292.10`
- Max drawdown fraction: `0.1822`
- Annualized run-rate from this training window: `$224408.94`

## Candidate Search Grid

- Target `40`: trades/day `39.87`, net `$160292.10`, drawdown `0.1822`, annualized `$224408.94`
- Target `35`: trades/day `34.93`, net `$140570.70`, drawdown `0.1621`, annualized `$196798.98`
- Target `30`: trades/day `29.97`, net `$119426.00`, drawdown `0.1494`, annualized `$167196.40`
- Target `25`: trades/day `24.99`, net `$99988.20`, drawdown `0.1437`, annualized `$139983.48`
- Target `50`: trades/day `49.76`, net `$200105.60`, drawdown `0.2175`, annualized `$280147.84`
- Target `45`: trades/day `44.82`, net `$180088.20`, drawdown `0.2004`, annualized `$252123.48`

## Train Window

- Date range: `2024-06-28` -> `2026-01-06`
- Selected available day folders: `180`
- Raw rows: `18734971`
- Aggregated session rows across all modeled sessions: `4809728`
- Raw candidate pool: `78409`
- Selected event candidates: `7137`
- Simulated trades: `7137`
- Win rate: `0.8142`
- Average trade PnL: `$22.46`
- Baseline max drawdown at 1 contract: `$1822.00`
- Dynamic contracts cap from 20% drawdown budget: `1`
- Ending balance: `$170292.10`
- Max drawdown dollars: `$1822.00`

## Session Mix

- Selected events from `Asia`: `4221`
- Selected events from `London`: `2552`
- Selected events from `New York`: `364`
- Realized trades from `Asia`: `4221`
- Realized trades from `London`: `2552`
- Realized trades from `New York`: `364`

## Notes

- V2 keeps the same strategy family and extends it across Asia, London, and New York rather than inventing a new unrelated setup.
- Daily selection is now global across all modeled sessions, which narrows the focus to the strongest same-day opportunities instead of forcing equal participation from each session.
- The annualized figure above is only a training-window run-rate projection from segmented history, not a validated yearly claim.
- The next honest step is to freeze this V2 configuration and test it on a later chronological validation block before making any live-quality performance claim.

