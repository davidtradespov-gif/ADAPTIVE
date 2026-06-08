# Strategy 01 Absorption Reversal Report

Related: [[ADAPTIVE]] | [[FIRST_STRATEGY_SPEC]] | [[Projects/ADAPTIVE/Strategy 01 - MGC Failed Auction Reversal]]

## Scope

- Instrument: `MGC`
- Sessions: `Asia, London, New York`
- Setup family: absorption reversal / failed continuation
- Account context: `10,000` sim
- Strategy target band: `25` to `50` trades per day with max `20%` drawdown

## Important Honesty Note

This report uses the segmented MGC dataset currently available in the repository. It is not a claim of a continuous recent six-month train plus one-year OOS sample.
The probability selector is still fit on the same candidate pool used to rank opportunities in this run, so this remains a strategy-construction result rather than a true validation result.
On 2026-06-08 the MGC tick-to-price and tick-to-dollar conversion bug in the backtester was corrected. Earlier Strategy 01 reports generated before that fix should be treated as invalid historical checkpoints rather than trusted performance evidence.

## V2 Search Outcome

- Selected trade target: `40` per day
- Runner variant: `base_runner_9`
- Average realized trades per day: `39.87`
- Net PnL: `$2902680.60`
- Max drawdown fraction: `0.1928`
- Annualized run-rate from this training window: `$4063752.84`

## Candidate Search Grid

- Target `40`, variant `base_runner_9`: trades/day `39.87`, net `$2902680.60`, drawdown `0.1928`, annualized `$4063752.84`

## Train Window

- Date range: `2024-06-28` -> `2026-01-06`
- Selected available day folders: `180`
- Raw rows: `18734971`
- Aggregated session rows across all modeled sessions: `4809728`
- Raw candidate pool: `78409`
- Selected event candidates: `7137`
- Simulated trades: `7137`
- Runner-qualified trades: `0`
- Runner-active trades: `0`
- Add-on trades: `0`
- Win rate: `0.3677`
- Average trade PnL: `$406.71`
- Baseline max drawdown at 1 contract: `$321.40`
- Dynamic contracts cap from 20% drawdown budget: `6`
- Ending balance: `$2912680.60`
- Max drawdown dollars: `$1928.40`

## Session Mix

- Selected events from `Asia`: `2502`
- Selected events from `London`: `3599`
- Selected events from `New York`: `1036`
- Realized trades from `Asia`: `2502`
- Realized trades from `London`: `3599`
- Realized trades from `New York`: `1036`

## Notes

- V2 keeps the same strategy family and extends it across Asia, London, and New York rather than inventing a new unrelated setup.
- Daily selection is now global across all modeled sessions, which narrows the focus to the strongest same-day opportunities instead of forcing equal participation from each session.
- Because the corrected contract math materially changed both PnL and which trades label as successful, the selected session mix and win rate also changed relative to the pre-fix report.
- The annualized figure above is only a training-window run-rate projection from segmented history, not a validated yearly claim.
- The next honest step is to freeze this V2 configuration and test it on a later chronological validation block before making any live-quality performance claim.

