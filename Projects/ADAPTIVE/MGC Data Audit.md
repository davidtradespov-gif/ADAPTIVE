# MGC Data Audit

Backlink: [[ADAPTIVE]]

## Summary

The first repeatable audit of the stored MGC COMEX historical trade package has been set up and run from inside the project.

## Workflow

- Audit script: `scripts/audit_mgc_dataset.py`
- Setup note: `docs/mgc_audit_setup.md`
- Report outputs:
  - `reports/mgc_data_audit.md`
  - `reports/mgc_data_audit.json`

## Confirmed Findings

- Day folders: `204`
- Parquet files: `198`
- Meta JSON files: `201`
- Kept rows from parquet: `19,701,740`
- Rows scanned before filtering: `66,277,273`
- Duplicate rows within single parquet files: `0`
- All observed `channel` values are null
- Timestamp range UTC: `2024-06-02T22:00:00+00:00` -> `2026-01-06T21:59:59.709105+00:00`
- Price range: `-333.0` -> `4876.8`

## Schema Sample

- `ticker`
- `timestamp`
- `sequence_number`
- `report_sequence`
- `price`
- `size`
- `channel`
- `session_end_date`

## Data-Quality Flags

- Empty day folders:
  - `date=2025-01-20`
  - `date=2025-02-17`
  - `date=2025-03-12`
  - `date=2025-06-19`
  - `date=2025-08-12`
  - `date=2026-01-07`
- Minimum observed price `-333.0` needs investigation before we trust all raw ticks blindly.
- The package includes many spread-style tickers, so we need a decision on whether the first baseline should filter to outright contracts only.
