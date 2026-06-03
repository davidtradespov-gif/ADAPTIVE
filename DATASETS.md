# Data Catalog

## MGC COMEX Gold Baseline

This is the canonical historical dataset for all Gold futures strategy research in `ADAPTIVE`.

### Primary Dataset

- Instrument: `MGC` Micro Gold futures
- Venue: `COMEX`
- Dataset type: historical trade tick data
- Local package root: `C:\Users\david\OneDrive - My Biologics Pty Ltd\Trading\ADAPTIVE\mgc_comex_trades_package (2)\mgc_comex_trades_package`
- Trade data root: `C:\Users\david\OneDrive - My Biologics Pty Ltd\Trading\ADAPTIVE\mgc_comex_trades_package (2)\mgc_comex_trades_package\trades_s3_mgc_parquet`

### Confirmed Package Facts

- Trading day folders: `204`
- First day: `2024-06-03`
- Last day: `2026-01-07`
- Parquet files found: `198`
- JSON files found: `201`
- Approximate parquet+json size: `287,984,544` bytes

### File Layout

- One folder per day: `date=YYYY-MM-DD`
- Parquet trade files within day folders
- Per-day JSON metadata files within day folders
- Package-level metadata:
  - `README.md`
  - `manifest.json`

### Usage Rule

- Treat this dataset as the default source for all MGC / Gold strategy research and backtests unless a later project note explicitly supersedes it.
- Keep raw package files inside `ADAPTIVE` and refer to them from research code rather than copying them around.

### Current Limitation

- Full parquet schema profiling is still pending because the bundled runtime currently lacks `pyarrow` or `fastparquet`.
- Before feature engineering, perform a full audit of columns, timestamps, duplicates, session continuity, timezone handling, and contract assumptions.
