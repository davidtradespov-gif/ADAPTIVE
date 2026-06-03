from __future__ import annotations

import json
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_PYTHON_PACKAGES = REPO_ROOT / ".python_packages"
if str(LOCAL_PYTHON_PACKAGES) not in sys.path:
    sys.path.insert(0, str(LOCAL_PYTHON_PACKAGES))

import pandas as pd


DATASET_ROOT = REPO_ROOT / "mgc_comex_trades_package (2)" / "mgc_comex_trades_package"
TRADES_ROOT = DATASET_ROOT / "trades_s3_mgc_parquet"
REPORTS_DIR = REPO_ROOT / "reports"
JSON_REPORT = REPORTS_DIR / "mgc_data_audit.json"
MARKDOWN_REPORT = REPORTS_DIR / "mgc_data_audit.md"


@dataclass
class FileAudit:
    path: str
    rows: int
    min_timestamp: int | None
    max_timestamp: int | None
    min_price: float | None
    max_price: float | None
    null_channel_rows: int
    duplicate_rows_in_file: int
    tickers: list[str]


def ns_to_iso(value: int | None) -> str | None:
    if value is None:
        return None
    seconds = value / 1_000_000_000
    return datetime.fromtimestamp(seconds, tz=UTC).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def audit_file(path: Path) -> FileAudit:
    df = pd.read_parquet(path)
    rows = int(len(df))
    min_timestamp = int(df["timestamp"].min()) if rows else None
    max_timestamp = int(df["timestamp"].max()) if rows else None
    min_price = float(df["price"].min()) if rows else None
    max_price = float(df["price"].max()) if rows else None
    null_channel_rows = int(df["channel"].isna().sum()) if "channel" in df.columns else 0
    duplicate_rows = int(df.duplicated().sum())
    tickers = sorted(df["ticker"].dropna().astype(str).unique().tolist()) if "ticker" in df.columns else []
    return FileAudit(
        path=str(path.relative_to(REPO_ROOT)),
        rows=rows,
        min_timestamp=min_timestamp,
        max_timestamp=max_timestamp,
        min_price=min_price,
        max_price=max_price,
        null_channel_rows=null_channel_rows,
        duplicate_rows_in_file=duplicate_rows,
        tickers=tickers,
    )


def build_report() -> dict[str, Any]:
    day_dirs = sorted([p for p in TRADES_ROOT.iterdir() if p.is_dir()])
    parquet_files = sorted(TRADES_ROOT.rglob("*.parquet"))
    meta_files = sorted(TRADES_ROOT.rglob("*_meta.json"))
    manifest = read_json(DATASET_ROOT / "manifest.json")

    folder_to_parquet_count = {
        str(day.relative_to(TRADES_ROOT)): len(list(day.glob("*.parquet"))) for day in day_dirs
    }
    empty_day_folders = sorted([day for day, count in folder_to_parquet_count.items() if count == 0])

    file_audits = [audit_file(path) for path in parquet_files]

    total_rows = sum(file.rows for file in file_audits)
    duplicate_rows = sum(file.duplicate_rows_in_file for file in file_audits)
    tickers = sorted({ticker for file in file_audits for ticker in file.tickers})
    min_timestamp = min((file.min_timestamp for file in file_audits if file.min_timestamp is not None), default=None)
    max_timestamp = max((file.max_timestamp for file in file_audits if file.max_timestamp is not None), default=None)
    min_price = min((file.min_price for file in file_audits if file.min_price is not None), default=None)
    max_price = max((file.max_price for file in file_audits if file.max_price is not None), default=None)
    null_channel_rows = sum(file.null_channel_rows for file in file_audits)

    schema_counter: Counter[tuple[tuple[str, str], ...]] = Counter()
    for path in parquet_files:
        df = pd.read_parquet(path, engine="pyarrow")
        schema_counter.update([tuple((name, str(dtype)) for name, dtype in df.dtypes.items())])
        break

    meta_examples = [read_json(path) for path in meta_files[:3]]
    kept_rows_total_from_meta = 0
    total_rows_scanned_from_meta = 0
    for path in meta_files:
        meta = read_json(path)
        kept_rows_total_from_meta += int(meta.get("kept_rows", 0))
        total_rows_scanned_from_meta += int(meta.get("total_rows_scanned", 0))

    report = {
        "generated_at_utc": datetime.now(tz=UTC).isoformat(),
        "dataset_root": str(DATASET_ROOT),
        "trades_root": str(TRADES_ROOT),
        "manifest": manifest,
        "day_folder_count": len(day_dirs),
        "parquet_file_count": len(parquet_files),
        "meta_json_count": len(meta_files),
        "empty_day_folders": empty_day_folders,
        "folder_to_parquet_count": folder_to_parquet_count,
        "totals": {
            "rows_from_parquet": total_rows,
            "kept_rows_from_meta": kept_rows_total_from_meta,
            "total_rows_scanned_from_meta": total_rows_scanned_from_meta,
            "duplicate_rows_within_files": duplicate_rows,
            "null_channel_rows": null_channel_rows,
            "unique_tickers": tickers,
            "min_timestamp_ns": min_timestamp,
            "max_timestamp_ns": max_timestamp,
            "min_timestamp_utc": ns_to_iso(min_timestamp),
            "max_timestamp_utc": ns_to_iso(max_timestamp),
            "min_price": min_price,
            "max_price": max_price,
        },
        "schema_sample": [list(item) for item in next(iter(schema_counter.keys()), ())],
        "meta_examples": meta_examples,
        "sample_files": [asdict(file) for file in file_audits[:5]],
    }
    return report


def write_markdown(report: dict[str, Any]) -> str:
    totals = report["totals"]
    lines = [
        "# MGC Data Audit",
        "",
        f"Generated: `{report['generated_at_utc']}`",
        "",
        "## Summary",
        "",
        f"- Dataset root: `{report['dataset_root']}`",
        f"- Day folders: `{report['day_folder_count']}`",
        f"- Parquet files: `{report['parquet_file_count']}`",
        f"- Meta JSON files: `{report['meta_json_count']}`",
        f"- Rows from parquet: `{totals['rows_from_parquet']}`",
        f"- Kept rows from meta: `{totals['kept_rows_from_meta']}`",
        f"- Total rows scanned from meta: `{totals['total_rows_scanned_from_meta']}`",
        f"- Duplicate rows within individual parquet files: `{totals['duplicate_rows_within_files']}`",
        f"- Unique tickers: `{', '.join(totals['unique_tickers'])}`",
        f"- Timestamp range UTC: `{totals['min_timestamp_utc']}` -> `{totals['max_timestamp_utc']}`",
        f"- Price range: `{totals['min_price']}` -> `{totals['max_price']}`",
        f"- Null `channel` rows: `{totals['null_channel_rows']}`",
        "",
        "## Schema Sample",
        "",
    ]
    for name, dtype in report["schema_sample"]:
        lines.append(f"- `{name}`: `{dtype}`")

    lines.extend(["", "## Empty Day Folders", ""])
    if report["empty_day_folders"]:
        for day in report["empty_day_folders"]:
            lines.append(f"- `{day}`")
    else:
        lines.append("- None")

    lines.extend(["", "## Sample Files", ""])
    for file in report["sample_files"]:
        lines.append(
            f"- `{file['path']}`: rows={file['rows']}, tickers={','.join(file['tickers'])}, "
            f"range={ns_to_iso(file['min_timestamp'])} -> {ns_to_iso(file['max_timestamp'])}"
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    report = build_report()
    JSON_REPORT.write_text(json.dumps(report, indent=2))
    MARKDOWN_REPORT.write_text(write_markdown(report))
    print(f"Wrote {JSON_REPORT}")
    print(f"Wrote {MARKDOWN_REPORT}")


if __name__ == "__main__":
    main()
