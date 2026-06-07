# ADAPTIVE Project State

Backlink: [[ADAPTIVE]]

## Summary

The project root is `C:\Users\smile\Documents\ADAPTIVE LOCAL BASED\ADAPTIVE`. Durable repo memory and the local Obsidian vault both live inside this folder.

## Current Status

- Repo memory files exist: `AGENTS.md`, `DATASETS.md`, `MEMORY.md`, `PROJECT_STATE.md`, `README.md`, `RESEARCH_PRINCIPLES.md`, `RUNBOOK.md`
- Full provided order-flow education context is stored in `Order Flow Education Context.md`
- First MGC audit findings are stored in `MGC Data Audit.md`
- Local Obsidian vault metadata exists under `.obsidian`
- `ADAPTIVE.md` is the hub note for graph navigation
- Git repo exists at the project root
- `origin` is configured only as `https://github.com/davidtradespov-gif/ADAPTIVE.git`
- GitHub repo is reachable and `main` has been pushed successfully
- MGC COMEX historical trade data is stored inside the project and is the default Gold research baseline
- A repeatable audit workflow now exists for the MGC package
- The current operating assumption is that the stored tick data is sufficient to begin backtesting work
- The first strategy thesis is now defined as a failed-auction reversal setup in MGC Gold
- The requested absorption-reversal build has a stored research brief with explicit data constraints
- A first executable Strategy 01 runner has now been built and run
- The current Strategy 01 build now stays under the requested `5%` drawdown ceiling on the `10,000` training simulation while meeting the `3` trades per day target
- A separate high-frequency Strategy 01 research variant now exists for the near-`30` trades/day objective
- The current high-frequency managed-exit build now fits the requested training-window target envelope on the full New York-session run
- The current local script and report match the canonical managed-exit high-frequency Strategy 01 checkpoint from commit `3fef09a`
- Strategy 01 V2 now extends the same logic family across Asia, London, and New York with global daily selection
- The accepted V2 training variant is the `40` trades/day target with about `$160292.10` net PnL and about `18.22%` max drawdown on the `10,000` simulation
- The next exact build step is to freeze this V2 training build and add the first true chronological validation block

## Immediate Next Steps

1. Freeze this high-frequency Strategy 01 training build and define the first true chronological validation block.
2. Stress-test the managed-exit version under worse slippage and commission assumptions.
3. Then extend the same logic family into London and Asia session research.
