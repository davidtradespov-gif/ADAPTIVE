# Research Principles

## Order Flow Build Standard

This project uses order-flow education and independent research only.

### Hard Boundaries

- Do not copy or reconstruct proprietary private strategy rules.
- Do not use private thresholds, time windows, feature sets, model logic, sizing policies, or execution behavior from another system.
- Build strategy logic from first principles, public market microstructure concepts, and validated project data.

### Core Research Rules

- Start from the available MGC data.
- Keep all validation chronological.
- Prevent look-ahead and train/test leakage.
- Include commissions, slippage, and conservative fill assumptions.
- Treat live trading as a separate engineering problem after research proves robust.
- Use order-flow concepts as hypotheses, not as assumed profitable rules.

### Default Build Path

1. Audit the MGC tick dataset.
2. Define a plain-English market hypothesis.
3. Define event timestamps and leakage-safe labels.
4. Build features only from information known at or before the event.
5. Split chronologically into train, validation, and test.
6. Calibrate probabilities if using ML.
7. Backtest net of costs.
8. Stress test across slippage, regimes, and walk-forward windows.

### Project Focus

- Initial market focus: Gold futures
- Initial instrument focus: `MGC`
- Initial research source: local MGC COMEX historical trade package inside `ADAPTIVE`
