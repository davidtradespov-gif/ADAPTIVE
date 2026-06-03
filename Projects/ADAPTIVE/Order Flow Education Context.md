# Order Flow Education Context

Backlink: [[ADAPTIVE]]

## Purpose

This note stores the full order-flow education context provided on 2026-06-04 for building an independent strategy research process inside `ADAPTIVE`.

It is educational only.

Do not copy, infer, reconstruct, or ask for any private strategy rules from another trading system. Build ideas from first principles, public market microstructure concepts, and properly validated project data.

## Hard Boundaries

Do not use or request:

- Any proprietary entry rule.
- Any proprietary exit rule.
- Any proprietary threshold.
- Any proprietary time window.
- Any proprietary feature set.
- Any proprietary model logic.
- Any proprietary sizing policy.
- Any proprietary prop-firm policy layer.
- Any proprietary execution bridge behavior.
- Any named private strategy, variant, or live system.

This note is not a strategy. It is a knowledge base for independent research.

## 1. What Order Flow Means

Order flow studies how buying and selling pressure enters the market.

A normal price chart shows where price went. Order flow tries to explain how it got there by looking at traded volume, aggressive buyers and sellers, liquidity, absorption, imbalance, and behavior around important price areas.

In futures markets, order flow usually means studying:

- Bid volume versus ask volume.
- Market buys lifting the offer.
- Market sells hitting the bid.
- Delta.
- Cumulative delta.
- Volume at price.
- Liquidity resting in the book.
- Pulling and stacking of liquidity.
- Absorption.
- Exhaustion.
- Failed auctions.
- Trapped traders.
- Breakout participation.
- Reversal pressure.

The goal is not to predict every tick. The goal is to identify moments where the market is structurally more likely to move favorably than unfavorably.

## 2. Core Auction Market Principles

Markets are auctions.

Price moves to find liquidity. When price is accepted, volume builds. When price is rejected, price often moves away quickly.

### Acceptance

Price spends time and volume in an area. This means both buyers and sellers are willing to trade there.

Signs of acceptance may include:

- High volume at price.
- Slow movement.
- Repeated two-way trade.
- Balanced delta.
- Price returning to the same area repeatedly.

### Rejection

Price enters an area and quickly leaves. This can show that one side had no interest continuing trade there.

Signs of rejection may include:

- Sharp move away from a level.
- Failed breakout.
- Low volume tail.
- Aggressive reversal after liquidity is touched.
- Delta failing to support price continuation.

### Value

Value is where the market agrees to trade. This can be defined in many ways:

- Volume profile high-volume nodes.
- VWAP region.
- Prior session value area.
- Opening range balance.
- Intraday consolidation.

### Imbalance

Imbalance happens when one side is clearly more aggressive or more urgent.

Examples:

- Buyers repeatedly lifting offers.
- Sellers repeatedly hitting bids.
- Delta expanding strongly.
- Price moving efficiently through low-volume zones.
- Liquidity being consumed faster than it replenishes.

### Failed Auction

A failed auction happens when price attempts to break higher or lower, but cannot attract enough continuation.

This can create strong reversal behavior because late traders become trapped.

## 3. Important Order Flow Concepts

### Delta

Delta is aggressive buying minus aggressive selling.

If trades happen at the ask, they are usually classified as buyer-initiated. If trades happen at the bid, they are usually classified as seller-initiated.

Positive delta means aggressive buyers dominated. Negative delta means aggressive sellers dominated.

But delta alone is not a signal. Context matters.

Examples:

- Positive delta with price rising can show healthy buying.
- Positive delta with price unable to rise can show absorption.
- Negative delta with price falling can show healthy selling.
- Negative delta with price unable to fall can show absorption.

### Cumulative Delta

Cumulative delta tracks delta over time.

It can be used to compare pressure against price.

Useful questions:

- Is price making new highs while cumulative delta confirms?
- Is price making new highs while cumulative delta diverges?
- Is selling pressure increasing but price not breaking down?
- Is buying pressure increasing but price not breaking out?

### Absorption

Absorption happens when aggressive orders hit the market, but price does not move as expected.

Example:

- Sellers hit the bid aggressively.
- Delta becomes very negative.
- Price stops falling.
- Buyers are passively absorbing the sell pressure.

Absorption can matter because it shows that one side is active but unable to move price.

### Exhaustion

Exhaustion happens when one side runs out of urgency.

Possible signs:

- Volume dries up at new highs or lows.
- Delta weakens.
- Breakout attempts fail.
- Price cannot continue despite prior momentum.
- Market makes a final push and stalls.

### Trapped Traders

Trapped traders enter in the wrong direction and are forced to exit.

Examples:

- Breakout buyers get trapped when price fails back inside range.
- Breakdown sellers get trapped when price reclaims a level.
- Late momentum traders enter after the move is exhausted.

Trapped traders can fuel sharp moves because exits become forced market orders.

### Liquidity Sweep

A liquidity sweep happens when price moves through an obvious level where stops or resting orders are likely located.

Common sweep areas:

- Prior high.
- Prior low.
- Opening range high or low.
- Overnight high or low.
- Session high or low.
- Equal highs or lows.
- Round numbers.

A sweep is not automatically a reversal. It can also be the start of continuation. The key question is whether price accepts or rejects after the sweep.

### Initiative Versus Responsive Activity

Initiative activity pushes price away from value.

Responsive activity fades price back toward value.

A trader should know whether they are trying to trade:

- Continuation from initiative pressure.
- Reversal from responsive rejection.
- Mean reversion inside balance.
- Breakout from balance.
- Failed breakout back into balance.

## 4. Useful Market Context

Order-flow signals are weak without context.

Before studying any entry idea, define the market state.

### Trend State

- Strong uptrend.
- Strong downtrend.
- Range.
- Rotational chop.
- Volatility expansion.
- Volatility compression.

### Location

Ask where price is:

- Near prior high.
- Near prior low.
- Near VWAP.
- Near value area high or low.
- Near overnight high or low.
- Near opening range.
- Near high-volume node.
- Near low-volume node.
- At fresh session extreme.
- In the middle of balance.

### Volatility

The same signal can behave differently in high and low volatility.

Measure things like:

- ATR.
- Bar range.
- Realized volatility.
- Distance from VWAP.
- Speed of movement.
- Session range expansion.

### Time of Day

Market behavior changes by session phase.

Do not blindly assume one rule works equally across:

- Open.
- Early trend discovery.
- Midday balance.
- Afternoon continuation.
- Closing flow.
- Overnight session.

Research this independently. Do not borrow proprietary time windows.

## 5. General Strategy Ideation Framework

A strategy idea should be described in plain English before code.

Use this structure:

### 1. Market Hypothesis

Example:

"When aggressive sellers fail to push price lower near an important liquidity area, the market may reverse upward because sellers are trapped and passive buyers are absorbing supply."

### 2. Setup Context

Define the environment where the idea should work.

Examples:

- Near an important prior level.
- After a liquidity sweep.
- During volatility expansion.
- After a failed breakout.
- Inside a range.
- At a value-area edge.
- During trend continuation.

### 3. Order Flow Confirmation

Define what evidence would support the idea.

Examples:

- Delta divergence.
- Absorption.
- Aggressive imbalance.
- Failed continuation.
- Reclaim of a level.
- Volume spike followed by rejection.
- Cumulative delta failing to confirm price.

### 4. Invalidation

Define what proves the idea wrong.

Examples:

- Price accepts beyond the level.
- Delta confirms continuation against the trade.
- Market fails to rotate away.
- Volatility expands against the idea.
- Liquidity does not respond as expected.

### 5. Exit Logic

Exit logic must be researched carefully.

Common educational exit categories:

- Fixed target and stop.
- Volatility-based stop.
- Structure-based stop.
- Time stop.
- Partial exit.
- Trail after favorable movement.
- Exit on opposing order-flow evidence.

Do not assume the best exit. Test it.

### 6. Risk Model

Decide risk before testing live.

Track:

- Average loss.
- Worst loss.
- Maximum drawdown.
- Losing streak.
- Daily loss.
- Position size.
- Commission.
- Slippage.
- Liquidity constraints.

## 6. Feature Ideas For Research

These are generic educational feature families, not strategy rules.

### Price Structure Features

- Return over multiple lookbacks.
- Distance from session open.
- Distance from prior high or low.
- Distance from VWAP.
- Distance from volume profile levels.
- Bar range.
- Wick size.
- Breakout or reclaim behavior.
- Consecutive higher highs or lower lows.

### Volume Features

- Volume spike.
- Relative volume.
- Volume at price.
- Session volume percentile.
- Volume concentration.
- Low-volume rejection areas.
- High-volume acceptance areas.

### Delta Features

- Bar delta.
- Rolling delta.
- Cumulative delta slope.
- Delta divergence from price.
- Delta acceleration.
- Delta exhaustion.
- Delta flip.

### Absorption Features

- Large negative delta with limited downside movement.
- Large positive delta with limited upside movement.
- Repeated failed pushes into a price zone.
- High volume with small price progress.
- Price holding despite aggressive pressure.

### Liquidity Features

If order book data is available:

- Bid or ask depth imbalance.
- Liquidity stacking.
- Liquidity pulling.
- Replenishment after trades.
- Spread.
- Book pressure near best bid or ask.
- Resting liquidity near key levels.

Historical depth data is harder to validate than bar data and can be vendor-specific.

### Session Features

- Time since open.
- Session phase.
- Day of week.
- Overnight range.
- Opening range behavior.
- Prior session relationship.
- News or high-volatility flags if available.

## 7. How To Build A Clean Research System

### Data Rules

Use the best data available, but be honest about its limits.

Possible data levels:

- 1-minute OHLCV.
- Tick trades.
- Bid or ask classified trades.
- Full market depth.
- Footprint or volumetric bars.

More detail is not automatically better. Bad tick or depth data can create false confidence.

### Chronological Split

Always split train and test chronologically.

Never randomly shuffle trades for final validation.

A safe structure:

- Earlier data for research and training.
- Later unseen data for testing.
- Final untouched data for out-of-sample confirmation.

### No Look-Ahead

Never use information from the future.

Common look-ahead traps:

- Using a bar's high and low without knowing which happened first.
- Using completed bar features for an entry that would occur inside the same bar.
- Using future session high or low.
- Optimizing on test data.
- Selecting thresholds after seeing test results.
- Using labels that leak future price movement into features.

### Commission And Slippage

All results must be net of costs.

At minimum include:

- Commission.
- Exchange fees.
- Realistic spread or slippage.
- Platform or execution assumptions.
- Missed fills if using limit orders.

Gross results are not enough.

### Fill Simulation

Fill simulation must respect time order.

If testing with 1-minute bars and both stop and target are touched inside the same bar, you cannot assume the favorable one hit first.

Better options:

- Use tick data.
- Use conservative same-bar assumptions.
- Drop ambiguous trades.
- Model intrabar path carefully.
- Validate fills with higher-resolution data.

## 8. Model-Based Probability Strategy Principles

If building an ML probability model, the model should estimate the probability that a trade idea goes favorably.

### Define The Event

An event is a possible trade opportunity.

Do not train on every bar unless that is intentional. Usually the model should evaluate moments where a setup could exist.

### Define The Label

The label should answer a specific question.

Examples:

- Did target hit before stop?
- Did price move favorably by X before adverse move Y?
- Was forward return positive after costs?
- Did the trade remain inside risk limits?

The label must match the intended trading decision.

### Calibrate Probabilities

If the model says 60 percent, then roughly 60 percent of those cases should succeed over time.

Use calibration methods such as:

- Platt scaling.
- Isotonic regression.
- Calibration curves.
- Reliability diagrams.
- Brier score.

Do not trust raw model scores as probabilities without calibration.

### Threshold Selection

A threshold is the minimum probability required to trade.

Thresholds must be selected on training and validation data, then tested on unseen later data.

Do not pick the threshold that looks best on the final test set.

### Interpretability

Track which feature families matter.

Useful checks:

- Feature importance.
- SHAP values.
- Permutation importance.
- Ablation tests.
- Regime-specific behavior.
- Stability over time.

If the model only works because of one fragile feature, treat it cautiously.

## 9. Backtesting Checklist

A serious backtest should answer:

- Is the split chronological?
- Is the test data unseen?
- Are costs included?
- Is fill logic conservative?
- Are ambiguous fills handled safely?
- Are probabilities calibrated?
- Was the threshold selected before final testing?
- Does performance survive different market regimes?
- Does it survive worse slippage?
- Does it survive reduced fill quality?
- Does it survive walk-forward testing?
- Does it survive Monte Carlo trade reshuffling?
- Does it survive daily-loss and drawdown constraints?
- Does it have enough trades to matter?
- Is the edge concentrated in only one day or one event?
- Is there a simple explanation for why it should work?

## 10. Common Failure Modes

### Overfitting

The strategy works only because it was tuned to the past.

Signs:

- Too many parameters.
- Tiny sample.
- Perfect-looking backtest.
- Weak forward performance.
- Thresholds selected from test data.
- Rules that only work in one narrow window.

### Fake Precision

Order flow can make traders feel they understand every tick. They do not.

Avoid making rules too specific unless the data proves they generalize.

### Ignoring Costs

Small scalps can disappear after commission and slippage.

Always test net performance.

### Confusing Absorption With Reversal

Absorption can lead to reversal, but it can also precede continuation after liquidity is fully consumed.

Require context and validation.

### Confusing Sweep With Reversal

A liquidity sweep is not automatically a fade. Sometimes it is continuation with strong initiative flow.

Study acceptance versus rejection after the sweep.

### Using Weak Data

If bid or ask classification is wrong, delta-based signals can be wrong.

Validate data quality before trusting order-flow features.

## 11. Good Independent Strategy Research Prompts

### Prompt 1: Build A Research Spec

"Help me write a plain-English research spec for an order-flow strategy idea based on public concepts only. The idea should include hypothesis, setup context, possible features, labels, invalidation, and validation plan. Do not use proprietary rules or thresholds."

### Prompt 2: Audit For Look-Ahead

"Review this backtest logic for look-ahead bias, intrabar fill assumptions, train or test leakage, threshold leakage, and missing commission or slippage."

### Prompt 3: Build A Feature Dataset

"Design a chronological feature dataset for futures order-flow research using only the data columns I provide. Include feature definitions, timestamp alignment rules, and leakage prevention."

### Prompt 4: Build A Label

"Help me define trade labels for whether a setup reaches target before stop, with true time-order handling and conservative ambiguous-fill behavior."

### Prompt 5: Calibration

"Help me evaluate whether my model probabilities are calibrated using reliability curves, Brier score, and bucketed win rates."

### Prompt 6: Strategy Robustness

"Help me build robustness tests: walk-forward splits, slippage stress, commission stress, Monte Carlo reshuffling, regime breakdown, and daily drawdown analysis."

## 12. Suggested Independent Build Path

### Phase 1: Data Audit

Confirm what data exists:

- OHLCV only.
- Tick trades.
- Bid or ask trades.
- Depth.
- Footprint bars.

Check timestamp quality, missing sessions, duplicate rows, timezone handling, and instrument rollover.

### Phase 2: Event Definition

Define when the system is allowed to evaluate a trade.

This could be based on generic public concepts like:

- Price near important levels.
- Volatility expansion.
- Liquidity sweep.
- Reclaim or failure behavior.
- Volume imbalance.
- Delta divergence.

Keep this broad at first.

### Phase 3: Labeling

Create labels that match the trade question.

Example:

"From this event timestamp, did price reach a favorable move before an adverse move within a fixed future horizon, net of costs?"

### Phase 4: Feature Engineering

Build features only from information known at or before the event timestamp.

Separate feature families:

- Price.
- Volume.
- Delta.
- Liquidity.
- Session context.
- Volatility.

### Phase 5: Baseline Model

Start simple:

- Logistic regression.
- Gradient boosted trees.
- Random forest.
- Calibrated classifier.

Do not begin with complex deep learning unless the simple models fail for a clear reason.

### Phase 6: Calibration

Calibrate the model and inspect whether predicted probabilities match realized outcomes.

### Phase 7: Threshold Sweep

Choose thresholds on training and validation only.

Then freeze the choice and test on later unseen data.

### Phase 8: Backtest

Backtest with conservative fills and all costs included.

### Phase 9: Stress Testing

Stress the system:

- Higher commission.
- Worse slippage.
- Missed fills.
- Lower liquidity.
- Randomized trade order.
- Bad days.
- Volatility regimes.
- Walk-forward windows.

### Phase 10: Paper Trade

Only after robust testing should the system be observed live in paper or sim mode.

Live observation should check:

- Signal timestamps.
- Data freshness.
- Fill realism.
- Platform behavior.
- Latency.
- Duplicate prevention.
- Kill switch behavior.
- Logging.

## 13. What A Good Strategy Thesis Looks Like

A good thesis is simple, testable, and falsifiable.

Example structure:

"When price enters an important liquidity area and aggressive pressure fails to continue price movement, trapped traders may be forced to exit. If the market then reclaims the failed area with improving participation, there may be a favorable short-term opportunity. This should only be valid when tested chronologically, net of costs, with conservative fill logic."

This is not a trading rule. It is a research thesis.

A real strategy still needs:

- Exact data definitions.
- Entry timing.
- Risk model.
- Exit model.
- Validation.
- Calibration.
- Robustness testing.
- Execution safety.

## 14. What Codex Should Never Do

Codex should not:

- Invent performance claims.
- Assume order-flow data is clean.
- Use future data in features.
- Randomly split time-series trades.
- Optimize on final test data.
- Ignore commissions.
- Assume high came before low inside a bar.
- Treat pretty backtests as proof.
- Copy private systems.
- Reverse-engineer someone else's live strategy from hints.

Codex should always:

- Ask what data columns exist.
- Preserve chronological order.
- Make assumptions explicit.
- Use conservative fills.
- Include costs.
- Separate train, validation, and test.
- Calibrate probabilities.
- Report blockers before upside.
- Treat live trading as a separate engineering problem.

## 15. Final Instruction To The Receiving Codex

You are being given general order-flow education only.

Your job is to help build an independent research process, not to reconstruct any private strategy.

Start from the user's available data, define a clean hypothesis, build leakage-safe features, create honest labels, split chronologically, calibrate probabilities, test net of all costs, and only then discuss whether the evidence is strong enough to continue.

If the user asks for secret thresholds, copied rules, private strategy logic, or anything owned by another system, refuse that part and redirect to independent research design.
