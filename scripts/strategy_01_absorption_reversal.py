from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from datetime import UTC
from pathlib import Path
from zoneinfo import ZoneInfo


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_PYTHON_PACKAGES = REPO_ROOT / ".python_packages"
if str(LOCAL_PYTHON_PACKAGES) not in sys.path:
    sys.path.insert(0, str(LOCAL_PYTHON_PACKAGES))

import pandas as pd


DATASET_ROOT = REPO_ROOT / "mgc_comex_trades_package (2)" / "mgc_comex_trades_package" / "trades_s3_mgc_parquet"
REPORTS_DIR = REPO_ROOT / "reports"
JSON_REPORT = REPORTS_DIR / "strategy_01_absorption_reversal_report.json"
MARKDOWN_REPORT = REPORTS_DIR / "strategy_01_absorption_reversal_report.md"
NEW_YORK_TZ = ZoneInfo("America/New_York")


@dataclass
class StrategyConfig:
    train_last_n_days: int = 180
    session_start_hour: int = 8
    session_end_hour: int = 13
    opening_range_minutes: int = 30
    rolling_window_trades: int = 90
    zscore_threshold: float = 1.9
    signed_flow_threshold: float = 70.0
    absorption_efficiency_cap: float = 0.30
    min_sweep_ticks: int = 0
    reclaim_ticks: int = 0
    rejection_seconds: int = 90
    cooldown_seconds: int = 210
    stop_ticks: int = 12
    target_ticks: int = 18
    max_hold_seconds: int = 600
    starting_balance: float = 10_000.0
    max_drawdown_fraction: float = 0.05
    per_contract_risk_dollars: float = 20.0
    target_risk_fraction_floor: float = 0.05
    target_risk_fraction_cap: float = 0.10
    commission_per_side: float = 0.85
    slippage_per_side_ticks: int = 1


def load_day(path: Path) -> pd.DataFrame:
    parts = sorted(path.glob("*.parquet"))
    if not parts:
        return pd.DataFrame()
    needed_columns = ["ticker", "timestamp", "price", "size"]
    df = pd.concat([pd.read_parquet(p, columns=needed_columns) for p in parts], ignore_index=True)
    if df.empty:
        return df
    df["ts_utc"] = pd.to_datetime(df["timestamp"], unit="ns", utc=True)
    df["ts_ny"] = df["ts_utc"].dt.tz_convert(NEW_YORK_TZ)
    df["is_spread"] = df["ticker"].astype(str).str.contains("-", regex=False)
    return df


def in_window(day_name: str, start: str, end: str) -> bool:
    date_value = day_name.split("=", 1)[1]
    return start <= date_value <= end


def load_window(start: str, end: str) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for day in sorted(p for p in DATASET_ROOT.iterdir() if p.is_dir()):
        if in_window(day.name, start, end):
            df = load_day(day)
            if not df.empty:
                frames.append(df)
    if not frames:
        return pd.DataFrame()
    result = pd.concat(frames, ignore_index=True)
    return result.sort_values("ts_utc").reset_index(drop=True)


def available_day_dirs() -> list[Path]:
    days = []
    for day in sorted(p for p in DATASET_ROOT.iterdir() if p.is_dir()):
        if any(day.glob("*.parquet")):
            days.append(day)
    return days


def select_last_n_available_days(n: int) -> tuple[str, str, list[str]]:
    days = available_day_dirs()
    selected = days[-n:] if len(days) > n else days
    selected_names = [p.name.split("=", 1)[1] for p in selected]
    return selected_names[0], selected_names[-1], selected_names


def filter_new_york_session(df: pd.DataFrame, cfg: StrategyConfig) -> pd.DataFrame:
    if df.empty:
        return df
    hours = df["ts_ny"].dt.hour
    result = df[(hours >= cfg.session_start_hour) & (hours < cfg.session_end_hour)].copy()
    result = result[~result["is_spread"]].copy()
    return result


def aggregate_session(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    work = df.sort_values("ts_utc").copy()
    work["ts_utc_sec"] = work["ts_utc"].dt.floor("s")
    work["ts_ny_sec"] = work["ts_ny"].dt.floor("s")
    work["price_change"] = work["price"].diff()
    work["signed_size"] = work["size"] * work["price_change"].fillna(0.0).apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    grouped = (
        work.groupby("ts_utc_sec", as_index=False)
        .agg(
            ts_ny=("ts_ny_sec", "last"),
            price=("price", "last"),
            high=("price", "max"),
            low=("price", "min"),
            volume=("size", "sum"),
            trades=("size", "count"),
            signed_flow=("signed_size", "sum"),
            ticker=("ticker", "last"),
        )
    )
    grouped["ts_utc"] = grouped["ts_utc_sec"]
    return grouped


def build_features(df: pd.DataFrame, cfg: StrategyConfig) -> pd.DataFrame:
    if df.empty:
        return df
    result = df.copy()
    session_start = result["ts_ny"].iloc[0]
    opening_range_end = session_start + pd.Timedelta(minutes=cfg.opening_range_minutes)
    result["price_change"] = result["price"].diff()
    result["price_range"] = result["high"] - result["low"]
    result["rolling_signed_flow"] = result["signed_flow"].rolling(cfg.rolling_window_trades, min_periods=20).sum()
    result["rolling_size_mean"] = result["volume"].rolling(cfg.rolling_window_trades, min_periods=20).mean()
    result["rolling_size_std"] = result["volume"].rolling(cfg.rolling_window_trades, min_periods=20).std()
    result["size_zscore"] = (
        (result["volume"] - result["rolling_size_mean"]) /
        result["rolling_size_std"].replace(0, pd.NA)
    ).fillna(0.0)
    result["rolling_high"] = result["high"].rolling(cfg.rolling_window_trades, min_periods=20).max().shift(1)
    result["rolling_low"] = result["low"].rolling(cfg.rolling_window_trades, min_periods=20).min().shift(1)
    result["cum_vwap_num"] = (result["price"] * result["volume"]).cumsum()
    result["cum_vwap_den"] = result["volume"].cumsum().replace(0, pd.NA)
    result["session_vwap"] = (result["cum_vwap_num"] / result["cum_vwap_den"]).ffill()
    opening_mask = result["ts_ny"] <= opening_range_end
    if opening_mask.any():
        opening_high = float(result.loc[opening_mask, "high"].max())
        opening_low = float(result.loc[opening_mask, "low"].min())
    else:
        opening_high = float(result["high"].iloc[0])
        opening_low = float(result["low"].iloc[0])
    result["opening_range_high"] = opening_high
    result["opening_range_low"] = opening_low
    result["distance_from_vwap"] = result["price"] - result["session_vwap"]
    result["absorption_efficiency"] = (
        result["price_range"] / result["volume"].replace(0, pd.NA)
    ).fillna(0.0)
    return result


def find_events(df: pd.DataFrame, cfg: StrategyConfig) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    candidates = []
    next_allowed_ts = None
    for i in range(cfg.rolling_window_trades, len(df) - 5):
        row = df.iloc[i]
        if next_allowed_ts is not None and row["ts_utc"] < next_allowed_ts:
            continue
        if row["size_zscore"] < cfg.zscore_threshold:
            continue
        if abs(float(row["rolling_signed_flow"])) < cfg.signed_flow_threshold:
            continue
        if float(row["absorption_efficiency"]) > cfg.absorption_efficiency_cap:
            continue
        prior_high = row["rolling_high"]
        prior_low = row["rolling_low"]
        if pd.isna(prior_high) or pd.isna(prior_low):
            continue
        prior_high = float(prior_high)
        prior_low = float(prior_low)
        opening_high = float(row["opening_range_high"])
        opening_low = float(row["opening_range_low"])
        high = float(row["high"])
        low = float(row["low"])
        price = float(row["price"])
        min_sweep = cfg.min_sweep_ticks
        reclaim = cfg.reclaim_ticks
        short_anchor = max(prior_high, opening_high)
        long_anchor = min(prior_low, opening_low)
        short_sweep = high >= short_anchor + min_sweep
        long_sweep = low <= long_anchor - min_sweep
        if short_sweep and price <= short_anchor - reclaim and row["rolling_signed_flow"] > 0 and price >= row["session_vwap"]:
            direction = "short"
            anchor = short_anchor
            sweep_price = high
        elif long_sweep and price >= long_anchor + reclaim and row["rolling_signed_flow"] < 0 and price <= row["session_vwap"]:
            direction = "long"
            anchor = long_anchor
            sweep_price = low
        else:
            continue
        cutoff = row["ts_utc"] + pd.Timedelta(seconds=cfg.rejection_seconds)
        future = df.iloc[i + 1:i + 120]
        future = future[future["ts_utc"] <= cutoff]
        if future.empty:
            continue
        if direction == "short":
            rejected = (future["price"] <= anchor - reclaim).any()
            entry_price = float(future.loc[future["price"] <= anchor - reclaim, "price"].iloc[0]) if rejected else None
        else:
            rejected = (future["price"] >= anchor + reclaim).any()
            entry_price = float(future.loc[future["price"] >= anchor + reclaim, "price"].iloc[0]) if rejected else None
        if not rejected or entry_price is None:
            continue
        next_allowed_ts = row["ts_utc"] + pd.Timedelta(seconds=cfg.cooldown_seconds)
        candidates.append({
            "event_ts_utc": row["ts_utc"].isoformat(),
            "event_ts_ny": row["ts_ny"].isoformat(),
            "direction": direction,
            "ticker": row["ticker"],
            "anchor_price": anchor,
            "event_price": price,
            "sweep_price": sweep_price,
            "entry_price": entry_price,
            "size": int(row["volume"]),
            "size_zscore": float(row["size_zscore"]),
            "rolling_signed_flow": float(row["rolling_signed_flow"]),
            "session_vwap": float(row["session_vwap"]),
        })
    return pd.DataFrame(candidates)


def simulate_trades(events: pd.DataFrame, full_df: pd.DataFrame, cfg: StrategyConfig) -> pd.DataFrame:
    if events.empty:
        return pd.DataFrame()
    trades = []
    tick_value = 1.0
    stop_distance = cfg.stop_ticks * tick_value
    target_distance = cfg.target_ticks * tick_value
    round_trip_cost = 2 * cfg.commission_per_side + 2 * cfg.slippage_per_side_ticks * tick_value
    full_df = full_df.sort_values("ts_utc").reset_index(drop=True)
    for _, event in events.iterrows():
        entry_ts = pd.Timestamp(event["event_ts_utc"])
        entry_price = float(event["entry_price"])
        direction = event["direction"]
        future = full_df[(full_df["ts_utc"] > entry_ts) & (full_df["ts_utc"] <= entry_ts + pd.Timedelta(seconds=cfg.max_hold_seconds))]
        if future.empty:
            continue
        exit_reason = "time"
        exit_price = float(future.iloc[-1]["price"])
        for _, row in future.iterrows():
            price = float(row["price"])
            if direction == "long":
                if price <= entry_price - stop_distance:
                    exit_price = entry_price - stop_distance
                    exit_reason = "stop"
                    break
                if price >= entry_price + target_distance:
                    exit_price = entry_price + target_distance
                    exit_reason = "target"
                    break
            else:
                if price >= entry_price + stop_distance:
                    exit_price = entry_price + stop_distance
                    exit_reason = "stop"
                    break
                if price <= entry_price - target_distance:
                    exit_price = entry_price - target_distance
                    exit_reason = "target"
                    break
        pnl_ticks = (exit_price - entry_price) if direction == "long" else (entry_price - exit_price)
        pnl_dollars = pnl_ticks * tick_value - round_trip_cost
        trades.append({
            "event_ts_utc": event["event_ts_utc"],
            "direction": direction,
            "ticker": event["ticker"],
            "entry_price": entry_price,
            "exit_price": exit_price,
            "exit_reason": exit_reason,
            "pnl_dollars_1_contract": pnl_dollars,
        })
    return pd.DataFrame(trades)


def evaluate_selected_days(selected_days: list[str], cfg: StrategyConfig) -> dict:
    total_raw_rows = 0
    total_session_rows = 0
    event_frames: list[pd.DataFrame] = []
    trade_frames: list[pd.DataFrame] = []
    for day_name in selected_days:
        day_path = DATASET_ROOT / f"date={day_name}"
        raw = load_day(day_path)
        if raw.empty:
            continue
        total_raw_rows += len(raw)
        session = filter_new_york_session(raw, cfg)
        if session.empty:
            continue
        aggregated = aggregate_session(session)
        total_session_rows += len(aggregated)
        features = build_features(aggregated, cfg)
        events = find_events(features, cfg)
        if not events.empty:
            trades = simulate_trades(events, aggregated, cfg)
            event_frames.append(events)
            if not trades.empty:
                trade_frames.append(trades)
    all_events = pd.concat(event_frames, ignore_index=True) if event_frames else pd.DataFrame()
    all_trades = pd.concat(trade_frames, ignore_index=True) if trade_frames else pd.DataFrame()
    sized = apply_dynamic_sizing(all_trades, cfg)
    return {
        "start": selected_days[0] if selected_days else None,
        "end": selected_days[-1] if selected_days else None,
        "selected_days": selected_days,
        "selected_day_count": len(selected_days),
        "raw_rows": int(total_raw_rows),
        "session_rows": int(total_session_rows),
        "events": int(len(all_events)),
        "trades": int(len(all_trades)),
        "summary": sized,
    }


def apply_dynamic_sizing(trades: pd.DataFrame, cfg: StrategyConfig) -> dict:
    if trades.empty:
        return {
            "trades": 0,
            "ending_balance": cfg.starting_balance,
            "max_drawdown_dollars": 0.0,
            "max_drawdown_fraction": 0.0,
            "avg_trades_per_day": 0.0,
            "net_pnl": 0.0,
            "contracts_cap": 0,
            "win_rate": 0.0,
            "avg_trade_pnl": 0.0,
            "baseline_max_drawdown_1_contract": 0.0,
        }
    baseline_equity = cfg.starting_balance
    baseline_peak = baseline_equity
    baseline_max_dd = 0.0
    for _, row in trades.iterrows():
        baseline_equity += row["pnl_dollars_1_contract"]
        baseline_peak = max(baseline_peak, baseline_equity)
        baseline_max_dd = max(baseline_max_dd, baseline_peak - baseline_equity)
    drawdown_budget = cfg.starting_balance * cfg.max_drawdown_fraction
    contracts_cap = max(1, math.floor(drawdown_budget / max(baseline_max_dd, cfg.per_contract_risk_dollars)))

    balance = cfg.starting_balance
    equity_peak = balance
    max_dd = 0.0
    trade_dates = {}
    realized = []
    for _, row in trades.iterrows():
        trade_date = row["event_ts_utc"][:10]
        trade_dates[trade_date] = trade_dates.get(trade_date, 0) + 1
        max_contracts = max(1, math.floor((balance * cfg.target_risk_fraction_cap) / cfg.per_contract_risk_dollars))
        min_contracts = max(1, math.floor((balance * cfg.target_risk_fraction_floor) / cfg.per_contract_risk_dollars))
        contracts = min(contracts_cap, max(1, min(max_contracts, max(min_contracts, 1))))
        pnl = row["pnl_dollars_1_contract"] * contracts
        balance += pnl
        equity_peak = max(equity_peak, balance)
        drawdown = equity_peak - balance
        max_dd = max(max_dd, drawdown)
        realized.append({
            **row.to_dict(),
            "contracts": contracts,
            "pnl_dollars": pnl,
            "balance_after": balance,
        })
    avg_trades_per_day = sum(trade_dates.values()) / max(1, len(trade_dates))
    pnl_values = [trade["pnl_dollars"] for trade in realized]
    return {
        "trades": len(realized),
        "ending_balance": balance,
        "max_drawdown_dollars": max_dd,
        "max_drawdown_fraction": max_dd / cfg.starting_balance,
        "avg_trades_per_day": avg_trades_per_day,
        "net_pnl": balance - cfg.starting_balance,
        "baseline_max_drawdown_1_contract": baseline_max_dd,
        "contracts_cap": contracts_cap,
        "win_rate": (sum(1 for value in pnl_values if value > 0) / len(pnl_values)) if pnl_values else 0.0,
        "avg_trade_pnl": (sum(pnl_values) / len(pnl_values)) if pnl_values else 0.0,
        "trade_details": realized[:25],
    }


def write_markdown(report: dict) -> str:
    lines = [
        "# Strategy 01 Absorption Reversal Report",
        "",
        "## Scope",
        "",
        "- Instrument: `MGC`",
        "- Session: New York only",
        "- Setup family: absorption reversal / failed continuation",
        "- Account context: `10,000` sim",
        "",
        "## Important Honesty Note",
        "",
        "This report uses the segmented MGC dataset currently available in the repository. It is not a claim of a continuous recent six-month train plus one-year OOS sample.",
        "",
    ]
    train = report["train"]
    summary = train["summary"]
    lines.extend([
        "## Train Window",
        "",
        f"- Date range: `{train['start']}` -> `{train['end']}`",
        f"- Selected available day folders: `{train['selected_day_count']}`",
        f"- Raw rows: `{train['raw_rows']}`",
        f"- New York session rows: `{train['session_rows']}`",
        f"- Event candidates: `{train['events']}`",
        f"- Simulated trades: `{train['trades']}`",
        f"- Average trades per day: `{summary['avg_trades_per_day']:.2f}`",
        f"- Win rate: `{summary['win_rate']:.4f}`",
        f"- Average trade PnL: `${summary['avg_trade_pnl']:.2f}`",
        f"- Baseline max drawdown at 1 contract: `${summary['baseline_max_drawdown_1_contract']:.2f}`",
        f"- Dynamic contracts cap from 5% drawdown budget: `{summary['contracts_cap']}`",
        f"- Net PnL: `${summary['net_pnl']:.2f}`",
        f"- Ending balance: `${summary['ending_balance']:.2f}`",
        f"- Max drawdown dollars: `${summary['max_drawdown_dollars']:.2f}`",
        f"- Max drawdown fraction: `{summary['max_drawdown_fraction']:.4f}`",
        "",
        "## Notes",
        "",
        "- This run trains on the last 180 available trading-day folders with parquet data, even though the underlying history is segmented.",
        "- No separate OOS block is claimed in this run because the current instruction is to build the strategy from the provided data.",
        "",
    ])
    return "\n".join(lines) + "\n"


def main() -> None:
    cfg = StrategyConfig()
    REPORTS_DIR.mkdir(exist_ok=True)
    train_start, train_end, selected_days = select_last_n_available_days(cfg.train_last_n_days)
    report = {
        "generated_at_utc": pd.Timestamp.now(tz=UTC).isoformat(),
        "config": cfg.__dict__,
        "train": evaluate_selected_days(selected_days, cfg),
    }
    JSON_REPORT.write_text(json.dumps(report, indent=2))
    MARKDOWN_REPORT.write_text(write_markdown(report))
    print(f"Wrote {JSON_REPORT}")
    print(f"Wrote {MARKDOWN_REPORT}")


if __name__ == "__main__":
    main()
